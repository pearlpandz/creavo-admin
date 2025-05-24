from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from ..models.license import License
from ..models.subscription import Subscription
from ..models.master_distributor import MasterDistributor
from ..models.distributor import Distributor
import uuid
from drf_spectacular.utils import extend_schema # type: ignore

@extend_schema(
    request={
        'application/json': {
            'type': 'object',
            'properties': {
                'master_distributor_id': {'type': 'integer'},
                'distributor_id': {'type': 'integer'},
                'subscriptions': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'subscription_id': {'type': 'integer'},
                            'quantity': {'type': 'integer'}
                        }
                    }
                }
            },
            'required': ['subscriptions']
        }
    },
    responses={
        201: {
            'type': 'object',
            'properties': {
                'generated_licenses': {
                    'type': 'array',
                    'items': {
                        'type': 'object',
                        'properties': {
                            'license_key': {'type': 'string'},
                            'subscription': {'type': 'string'}
                        }
                    }
                }
            }
        }
    }
)
class LicenseGeneratorAPIView(APIView):
    permission_classes = [IsAuthenticated]

    def post(self, request):
        data = request.data
        master_distributor_id = data.get('master_distributor_id')
        distributor_id = data.get('distributor_id')
        subscriptions = data.get('subscriptions', [])  # List of {"subscription_id": 1, "quantity": 5}

        if not master_distributor_id and not distributor_id:
            return Response({"error": "Either master_distributor_id or distributor_id must be provided."}, status=400)

        owner = None
        isMaster = False
        if master_distributor_id:
            isMaster = True
            owner = MasterDistributor.objects.filter(id=master_distributor_id).first()
        elif distributor_id:
            owner = Distributor.objects.filter(id=distributor_id).first()

        if not owner:
            return Response({"error": "Invalid master_distributor_id or distributor_id."}, status=400)

        generated_licenses = []

        for sub in subscriptions:
            subscription_id = sub.get('subscription_id')
            quantity = sub.get('quantity', 0)

            subscription = Subscription.objects.filter(id=subscription_id).first()
            if not subscription:
                return Response({"error": f"Invalid subscription_id: {subscription_id}"}, status=400)

            for _ in range(quantity):
                license_key = uuid.uuid4()
                license_obj = License.objects.create(
                    code=license_key,
                    subscription=subscription,
                    issued_to_distributor= None if isMaster else owner,
                    issued_to_master_distributor= owner if isMaster else None,
                    purchased_by= None
                )
                generated_licenses.append({
                    "code": license_obj.code,
                    "subscription": subscription.name
                })

        return Response({"generated_licenses": generated_licenses}, status=201)
