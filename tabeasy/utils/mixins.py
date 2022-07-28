import django.contrib.auth.mixins


class JudgeOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only judges can access this page"

    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_judge


class TeamOnlyMixin(django.contrib.auth.mixins.UserPassesTestMixin):
    permission_denied_message = "Only teams can access this page"

    def test_func(self):
        return self.request.user.is_authenticated \
               and self.request.user.is_team
