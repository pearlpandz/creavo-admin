from .models import PageSection, Project, Service, Testimonial, Blog

CMS_CONFIG = {
    "home": {
        "single": {
            "hero": "hero_section",
            "why_choose_us": "why_choose_us",
        },
        "multi": {
            "projects": Project,
            "services": Service,
            "testimonials": Testimonial,
            "blogs": Blog,
        }
    },

    "about": {
        "single": {
            "header": "header",
            "mission": "mission",
        },
        "multi": {}
    },

    # add more pages easily...
}
