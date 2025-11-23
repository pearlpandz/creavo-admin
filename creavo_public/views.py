import os
from django.conf import settings
from rest_framework import status, viewsets, mixins
from rest_framework.decorators import action, api_view, permission_classes
from rest_framework.response import Response
from rest_framework.parsers import MultiPartParser, FormParser
from .models import (ContactInquiry, NewsletterSubscriber, MediaLibrary, PageSection,
                     Project, Service, ServiceFeature, Template, TemplateCategory,
                     Testimonial, SiteSetting)
from .serializers import (ContactInquirySerializer, NewsletterSubscriberSerializer,
                          MediaLibrarySerializer, PageSectionSerializer, ProjectSerializer,
                          ServiceSerializer, ServiceFeatureSerializer, TemplateSerializer,
                          TemplateCategorySerializer, TestimonialSerializer, SiteSettingSerializer)
from rest_framework.views import APIView
from rest_framework.response import Response
from .models import PageSection, Project, Service, Testimonial, Blog
from .serializers import (
    PageSectionSerializer, ProjectSerializer, ServiceSerializer,
    TestimonialSerializer, BlogSerializer
)
from .cms_config import CMS_CONFIG
# Contact endpoints
class ContactViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin):
    queryset = ContactInquiry.objects.all()
    serializer_class = ContactInquirySerializer

    # POST /api/contact/ => create
    # GET /api/contact/inquiries/  -> admin, but we skip auth: restrict via host middleware or later
    @action(detail=False, methods=['get'], url_path='inquiries')
    def inquiries(self, request):
        status_q = request.query_params.get('status')
        qs = self.queryset
        if status_q:
            qs = qs.filter(status=status_q)
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        if limit:
            qs = qs[:int(limit)]
        serializer = self.get_serializer(qs, many=True)
        return Response(serializer.data)

    @action(detail=True, methods=['put'], url_path='status')
    def update_status(self, request, pk=None):
        # admin-only in node; we skip auth, but you can protect with middleware or IP check
        inquiry = self.get_object()
        new_status = request.data.get('status')
        if new_status not in dict(ContactInquiry.STATUS_CHOICES):
            return Response({'error': 'Invalid status'}, status=400)
        inquiry.status = new_status
        inquiry.save()
        return Response(self.get_serializer(inquiry).data)

# Newsletter
class NewsletterViewSet(viewsets.GenericViewSet, mixins.CreateModelMixin, mixins.ListModelMixin):
    queryset = NewsletterSubscriber.objects.all()
    serializer_class = NewsletterSubscriberSerializer

    @action(detail=False, methods=['post'], url_path='unsubscribe')
    def unsubscribe(self, request):
        email = request.data.get('email')
        NewsletterSubscriber.objects.filter(email=email).update(is_active=False)
        return Response({'message':'Successfully unsubscribed'})

# Media upload + listing
class MediaViewSet(viewsets.ViewSet):
    parser_classes = (MultiPartParser, FormParser)

    def list(self, request):
        q = MediaLibrary.objects.all().order_by('-created_at')
        # optional filters
        file_type = request.query_params.get('type')
        if file_type:
            q = q.filter(file_type__startswith=file_type)
        limit = request.query_params.get('limit')
        offset = request.query_params.get('offset')
        if limit:
            offset = int(offset or 0)
            q = q[offset: offset + int(limit)]
        serializer = MediaLibrarySerializer(q, many=True)
        return Response(serializer.data)

    def retrieve(self, request, pk=None):
        try:
            obj = MediaLibrary.objects.get(pk=pk)
        except MediaLibrary.DoesNotExist:
            return Response(status=404)
        serializer = MediaLibrarySerializer(obj)
        return Response(serializer.data)

    def create(self, request):
        # public upload in node had auth; skip auth or protect via origin middleware
        uploaded_file = request.FILES.get('file')
        if not uploaded_file:
            return Response({'error':'No file uploaded'}, status=400)
        # Save file to MEDIA_ROOT/uploads
        upload_root = os.path.join(settings.MEDIA_ROOT, 'uploads')
        os.makedirs(upload_root, exist_ok=True)
        fname = f"{uploaded_file.field_name}-{int(round(os.times()[4]*1000))}-{uploaded_file.name}"
        dest_path = os.path.join(upload_root, fname)
        with open(dest_path, 'wb+') as dest:
            for chunk in uploaded_file.chunks():
                dest.write(chunk)
        # Save DB record
        ml = MediaLibrary.objects.create(
            file_name=uploaded_file.name,
            file_path=dest_path,
            file_type=uploaded_file.content_type,
            file_size=uploaded_file.size,
            alt_text=request.data.get('alt_text',''),
            uploaded_by=request.data.get('uploaded_by','')
        )
        serializer = MediaLibrarySerializer(ml)
        return Response(serializer.data, status=201)

    def destroy(self, request, pk=None):
        try:
            obj = MediaLibrary.objects.get(pk=pk)
        except MediaLibrary.DoesNotExist:
            return Response(status=404)
        # delete file from filesystem
        if os.path.exists(obj.file_path):
            os.remove(obj.file_path)
        obj.delete()
        return Response({'message':'deleted'})

# Pages endpoint
class PageSectionViewSet(viewsets.ViewSet):
    def list(self, request):
        # GET /api/pages/
        from django.db import connection
        qs = PageSection.objects.order_by('page_name').values('page_name').distinct()
        pages = []
        for p in qs:
            sections = PageSection.objects.filter(page_name=p['page_name']).order_by('display_order','section_name')
            pages.append({'page_name': p['page_name'], 'sections': PageSectionSerializer(sections, many=True).data})
        return Response(pages)

    def retrieve(self, request, pk=None):
        # pk expected as pageName
        sections = PageSection.objects.filter(page_name=pk).order_by('display_order','section_name')
        return Response(PageSectionSerializer(sections, many=True).data)

    @action(detail=True, methods=['post','put','delete'], url_path='section')
    def manage_section(self, request, pk=None):
        # require admin in node; here it's public or guarded by middleware
        pageName = pk
        sectionName = request.data.get('section_name')
        if request.method == 'POST':
            # create or update
            obj, created = PageSection.objects.update_or_create(
                page_name=pageName, section_name=sectionName,
                defaults={
                    'content': request.data.get('content',''),
                    'content_type': request.data.get('content_type','html'),
                    'display_order': request.data.get('display_order',0),
                    'is_active': request.data.get('is_active',True)
                }
            )
            return Response(PageSectionSerializer(obj).data)
        elif request.method == 'DELETE':
            PageSection.objects.filter(page_name=pageName, section_name=sectionName).delete()
            return Response({'message':'deleted'})

# Projects, Services, Templates, Testimonials, Settings: use ModelViewSet for CRUD
from rest_framework import routers, mixins, viewsets
class ProjectViewSet(viewsets.ModelViewSet):
    queryset = Project.objects.filter(is_active=True)
    serializer_class = ProjectSerializer

class ServiceViewSet(viewsets.ModelViewSet):
    queryset = Service.objects.filter(is_active=True)
    serializer_class = ServiceSerializer

class TemplateViewSet(viewsets.ModelViewSet):
    queryset = Template.objects.filter(is_active=True)
    serializer_class = TemplateSerializer

class TemplateCategoryViewSet(viewsets.ModelViewSet):
    queryset = TemplateCategory.objects.filter(is_active=True)
    serializer_class = TemplateCategorySerializer

class TestimonialViewSet(viewsets.ModelViewSet):
    queryset = Testimonial.objects.filter(is_active=True)
    serializer_class = TestimonialSerializer

class SettingsViewSet(viewsets.ViewSet):
    def list(self, request):
        settings_q = SiteSetting.objects.all()
        data = {}
        for s in settings_q:
            v = s.setting_value
            if s.setting_type == 'json':
                import json
                try:
                    v = json.loads(v)
                except:
                    pass
            elif s.setting_type == 'number':
                try:
                    v = float(v)
                except:
                    pass
            elif s.setting_type == 'boolean':
                v = (v == 'true' or v == '1')
            data[s.setting_key] = v
        return Response(data)

    def retrieve(self, request, pk=None):
        try:
            s = SiteSetting.objects.get(setting_key=pk)
            val = s.setting_value
            if s.setting_type == 'json':
                import json
                try:
                    val = json.loads(val)
                except:
                    pass
            return Response({'key': s.setting_key, 'value': val, 'type': s.setting_type})
        except SiteSetting.DoesNotExist:
            return Response(status=404)

    def update(self, request, pk=None):
        # admin only in node; here skip auth or protect with middleware as needed
        val = request.data.get('value')
        t = request.data.get('type','text')
        if isinstance(val, (dict, list)):
            import json
            val_str = json.dumps(val)
        else:
            val_str = str(val)
        obj, created = SiteSetting.objects.update_or_create(setting_key=pk, defaults={'setting_value': val_str, 'setting_type': t})
        return Response({'message':'saved'})

MODEL_SERIALIZER_MAP = {
    "Project": ProjectSerializer,
    "Service": ServiceSerializer,
    "Testimonial": TestimonialSerializer,
    # "Blog": BlogSerializer,
}


class CMSPageAPI(APIView):

    def get(self, request):
        print("CMS API HIT")   
        page = request.GET.get("page")
        if not page:
            return Response({"error": "Missing ?page="}, status=400)

        if page not in CMS_CONFIG:
            return Response({"error": "Invalid page"}, status=404)

        config = CMS_CONFIG[page]
        response = {"page": page, "sections": {}}

        # ---------------------------
        # SINGLE SECTIONS
        # ---------------------------
        for key, section_name in config["single"].items():
            section = PageSection.objects.filter(
                page_name=page, section_name=section_name, is_active=True
            ).first()

            response["sections"][key] = (
                PageSectionSerializer(section).data if section else {}
            )

        # ---------------------------
        # MULTIPLE SECTIONS (Dynamic)
        # ---------------------------
        for key, model_class in config["multi"].items():

            model_name = model_class.__name__
            serializer_class = MODEL_SERIALIZER_MAP.get(model_name)

            if not serializer_class:
                response["sections"][key] = []
                continue

            qs = model_class.objects.filter(is_active=True).order_by("display_order" if hasattr(model_class, "display_order") else "id")
            response["sections"][key] = serializer_class(qs, many=True).data

        return Response(response)