from rest_framework.permissions import IsAuthenticated

from common.mixins import BaseDetailedCreateApiViewMixin
from common.api.default import DefaultRetrieveApiView, DefaultCreateApiView

from referrals.repositories.referral import ReferralRepository, \
    ReferrRepository


class ReferalStatusRetrieveAPIView(DefaultRetrieveApiView):
    repository = ReferralRepository()
    permission_classes = [IsAuthenticated]

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get(referral_id=self.request.user.id)
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


class AddLoseFundsApiView(BaseDetailedCreateApiViewMixin,
                          DefaultCreateApiView):
    repository = ReferrRepository()
    permission_classes = [IsAuthenticated]

    def create(self, request, *args, **kwargs):
        saved = self.repository.add_referr_funds(
            referral_id=request.user.id,
                advantage_diff=request.data.get("advantage_diff")
        )

        return self.get_201_response(data=saved)
