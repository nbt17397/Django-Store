from django.contrib import admin
from .models import AdditionalWork, BoxChat, Category, Department, Document, Message, Position, Process, Project, Stage, Step, User, Work

admin.site.register(User)
admin.site.register(Department)
admin.site.register(Project)
admin.site.register(Stage)
admin.site.register(Category)
admin.site.register(Position)
admin.site.register(BoxChat)
admin.site.register(Message)
admin.site.register(Step)
admin.site.register(Process)
admin.site.register(Work)
admin.site.register(AdditionalWork)
admin.site.register(Document)
