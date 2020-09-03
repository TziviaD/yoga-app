from django.contrib.auth.tokens import PasswordResetTokenGenerator





class SignupTokenGenerator(PasswordResetTokenGenerator):
    def _make_hash_value(self, profile, timestamp):
        return str(profile.pk) + str(timestamp) 

signup_account_token = SignupTokenGenerator()