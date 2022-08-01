from django.db import models
from django.contrib.auth.models import AbstractUser
from django.forms import IntegerField


class User(AbstractUser):
    class Meta:
        unique_together = ['email', 'department_id']

    avatar = models.ImageField(
        upload_to='project/uploads/%Y/%m', default=None)
    department_id = models.ForeignKey(
        'Department', on_delete=models.SET_NULL, null=True)
    manager_id = models.ForeignKey(
        'User', on_delete=models.SET_NULL, null=True)
    pos = models.CharField(max_length=100, null=False)
    address = models.CharField(max_length=200, null=True)
    isPM = models.BooleanField(default=True)
    device_token = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.first_name + ' ' + self.last_name


class ItemBase(models.Model):
    class Meta:
        abstract = True
    created_date = models.DateTimeField(auto_now_add=True)
    updated_date = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)


class Department(ItemBase):
    class Meta:
        unique_together = ['manager', 'department_name']

    department_name = models.CharField(max_length=150, null=False)
    manager = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(seft):
        return seft.department_name


class Project(ItemBase):
    class Meta:
        unique_together = ['project_name', 'department']

    project_name = models.CharField(max_length=200, null=False)
    project_code = models.CharField(max_length=50, null=False)
    status = models.IntegerField(null=False, default=1)
    is_important = models.BooleanField(default=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    complete_date = models.DateField(null=True)
    department = models.ForeignKey(
        Department, null=False, on_delete=models.PROTECT)
    users = models.ManyToManyField(
        "User", related_name="user_project", blank=True)
    project_manager = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True)

    def __str__(seft):
        return seft.project_name


class Stage(ItemBase):
    class Meta:
        unique_together = ['stage_name', 'project']

    stage_name = models.CharField(max_length=200, null=False)
    pos = models.IntegerField(default=1)
    project = models.ForeignKey(
        Project,  related_name="stages", on_delete=models.PROTECT, null=False)

    def __str__(self) -> str:
        return self.stage_name


class Category(ItemBase):
    class Meta:
        unique_together = ['category_name', 'stage']

    stage = models.ForeignKey(
        Stage, on_delete=models.PROTECT, related_name="categories", null=False)
    category_name = models.CharField(max_length=200, null=False)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    complete_date = models.DateTimeField(null=True)
    cost = models.FloatField(default=0)
    desc = models.TextField(null=True, blank=True)

    def __str__(self) -> str:
        return self.category_name


class Position(ItemBase):
    class Meta:
        unique_together = ['category', 'user', 'position_name']

    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="positions", null=False)
    position_name = models.CharField(max_length=50, null=False)
    color = models.CharField(max_length=200, null=False)
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=False)

    def __str__(self) -> str:
        return self.position_name


class BoxChat(ItemBase):

    category = models.OneToOneField(
        Category, on_delete=models.CASCADE, null=True)
    users = models.ManyToManyField(
        'User', related_name='user_boxchat', blank=True)


class Message(ItemBase):

    content = models.TextField(null=False)
    creator = models.ForeignKey(User, on_delete=models.CASCADE, null=False)
    box_chat = models.ForeignKey(
        BoxChat, on_delete=models.CASCADE, related_name="messages", null=False)


class Process(ItemBase):

    isExtra = models.BooleanField(default=True)
    desc = models.TextField(null=True)
    process_name = models.CharField(max_length=200, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def __str__(self) -> str:
        return self.process_name


class Step(ItemBase):

    step_name = models.CharField(max_length=200, null=False)
    desc = models.TextField(null=True)
    process = models.ForeignKey(
        Process, on_delete=models.CASCADE, related_name="steps", null=True)
    user_accept = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    users_notification = models.ManyToManyField(
        'User', related_name='user_notification', blank=True)
    isAccept = models.BooleanField(default=False)
    status = models.BooleanField(default=False)

    def __str__(self) -> str:
        return self.step_name


class Work(ItemBase):

    work_name = models.CharField(max_length=200, null=False)
    desc = models.TextField(null=True)
    status = models.BooleanField(default=False)
    isProcess = models.BooleanField(default=False)
    cost = models.FloatField(default=0)
    start_date = models.DateTimeField()
    end_date = models.DateTimeField()
    complete_date = models.DateTimeField(null=True)
    users = models.ManyToManyField(
        "User", related_name="user_work", blank=True)
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.CASCADE, related_name="works", null=True)

    def __str__(self) -> str:
        return self.work_name


class AdditionalWork(ItemBase):

    additional_name = models.CharField(max_length=200, null=False)
    desc = models.TextField(null=True)
    user_accept = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    users_notification = models.ManyToManyField(
        'User', related_name='user_noti',  blank=True)
    status = models.BooleanField(default=False)
    work = models.ForeignKey(
        Work, on_delete=models.CASCADE, related_name="add_works", null=True)

    def __str__(self) -> str:
        return self.additional_name


class Document(ItemBase):

    document_name = models.CharField(max_length=200, null=False)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    isWork = models.BooleanField(null=False, default=False)
    process = models.ForeignKey(Process, on_delete=models.SET_NULL, null=True)
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True)
    file = models.FileField(upload_to='documents/%Y/%m', default=None)

    def __str__(self) -> str:
        return self.document_name


class Notification(ItemBase):

    CREATE_CATE, COMPLETED_CATE, CREATE_WORK, COMPLETED_WORK = range(4)

    ACTIONS = [
        (CREATE_CATE, 'create_cate'),
        (COMPLETED_CATE, 'completed_cate'),
        (CREATE_WORK, 'create_work'),
        (COMPLETED_WORK, 'completed_work')
    ]

    content = models.CharField(max_length=200, null=False)
    work = models.ForeignKey(Work, on_delete=models.SET_NULL, null=True)
    category = models.ForeignKey(
        Category, on_delete=models.SET_NULL, null=True)
    project = models.ForeignKey(Project, on_delete=models.CASCADE, null=True)
    type = models.PositiveSmallIntegerField(
        choices=ACTIONS, default=CREATE_CATE)
    creator = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
