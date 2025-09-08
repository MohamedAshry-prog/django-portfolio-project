from django.contrib.auth.mixins import UserPassesTestMixin

class IsAdminMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'ADMIN'

class IsGeneralManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'GENERAL_MANAGER'

class IsDepartmentManagerMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'DEPARTMENT_MANAGER'

class IsEmployeeMixin(UserPassesTestMixin):
    def test_func(self):
        return self.request.user.role == 'EMPLOYEE'