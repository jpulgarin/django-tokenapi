# django.contrib.auth.tokens, but without using last_login in hash

from datetime import date
from django.conf import settings
from django.utils.http import int_to_base36, base36_to_int

class TokenGenerator(object):
    """
    Strategy object used to generate and check tokens
    """

    TOKEN_TIMEOUT_DAYS = getattr(settings, "TOKEN_TIMEOUT_DAYS", 7)

    def make_token(self, user):
        """
        Returns a token for a given user
        """
        return self._make_token_with_timestamp(user, self._num_days(self._today()))

    def check_token(self, user, token):
        """
        Check that a token is correct for a given user.
        """
        # Parse the token
        try:
            ts_b36, hash = token.split("-")
        except ValueError:
            return False

        try:
            ts = base36_to_int(ts_b36)
        except ValueError:
            return False

        # Check that the timestamp/uid has not been tampered with
        if self._make_token_with_timestamp(user, ts) != token:
            return False

        # Check the timestamp is within limit
        if (self._num_days(self._today()) - ts) > self.TOKEN_TIMEOUT_DAYS:
            return False

        return True

    def _make_token_with_timestamp(self, user, timestamp):
        # timestamp is number of days since 2001-1-1.  Converted to
        # base 36, this gives us a 3 digit string until about 2121
        ts_b36 = int_to_base36(timestamp)

        # No longer using last login time
        from django.utils.hashcompat import sha_constructor
        hash = sha_constructor(settings.SECRET_KEY + unicode(user.id) +
            user.password + 
            unicode(timestamp)).hexdigest()[::2]
        return "%s-%s" % (ts_b36, hash)

    def _num_days(self, dt):
        return (dt - date(2001,1,1)).days

    def _today(self):
        # Used for mocking in tests
        return date.today()


token_generator = TokenGenerator()
