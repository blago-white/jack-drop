from rest_framework.permissions import IsAuthenticated

from common.mixins import BaseDetailedCreateApiViewMixin
from common.api.default import DefaultRetrieveApiView, DefaultCreateApiView

from referrals.repositories.referral import ReferralRepository, ReferrRepository


class ReferalStatusRetrieveAPIView(DefaultRetrieveApiView):
    repository = ReferralRepository()
    pk_url_kwarg = "referr_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get(referral_id=self.get_requested_pk())
        )


class AddReferrApiView(BaseDetailedCreateApiViewMixin,
                       DefaultCreateApiView):
    repository = ReferrRepository()
    serializer_class = repository.default_serializer_class
    pk_url_kwarg = "referr_link"
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        saved = self.repository.add_referr(user_id=self.request.user.pk,
                                           referr_link=self.get_requested_pk_body())

        return self.get_201_response(data=saved)

    def get_queryset(self):
        return
