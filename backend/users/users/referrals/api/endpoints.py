from common.api.default import DefaultRetrieveApiView
from referrals.repositories.referral import ReferralRepository


class ReferalStatusRetrieveAPIView(DefaultRetrieveApiView):
    repository = ReferralRepository()
    pk_url_kwarg = "referr_id"

    def retrieve(self, request, *args, **kwargs):
        return self.get_200_response(
            data=self.repository.get(referral_id=self.get_requested_pk())
        )
