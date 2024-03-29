from rest_framework.serializers import ModelSerializer, SerializerMethodField, PrimaryKeyRelatedField
from .models import AdditionalWork, BoxChat, Department, Document, Message, Notification, Position, Process, Project, Stage, Step, User, Category, Work


class UserSerializer(ModelSerializer):

    class Meta:
        model = User
        fields = ["id", "first_name", "last_name", "email",
                  "username", "password", "manager_id", "department_id", "isPM", "avatar"]
        extra_kwargs = {
            'password': {'write_only': 'true'}
        }

    def create(self, validated_data):
        user = User(**validated_data)
        user.set_password(validated_data['password'])
        user.save()

        return user


class DepartmentSerializer(ModelSerializer):

    class Meta:
        model = Department
        fields = ["id", "department_name", "manager"]


class ProjectSerializer(ModelSerializer):
    users = UserSerializer(many=True, required=False, read_only=True)
    department = Department
    project_manager = UserSerializer

    class Meta:
        model = Project
        fields = ["id", "project_name", "project_code", "status", "is_important",
                  "start_date", "end_date", "complete_date", "department", "users", "project_manager"]


class StageSerializer(ModelSerializer):
    project = ProjectSerializer

    class Meta:
        model = Stage
        fields = ["id", "stage_name", "pos", "project", "categories"]


class CategorySerializer(ModelSerializer):
    stage = StageSerializer

    class Meta:
        model = Category
        fields = ["id", "category_name", "start_date",
                  "end_date", "complete_date", "cost", "desc", "stage"]



class PositionSerializer(ModelSerializer):
    category = CategorySerializer
    user = UserSerializer

    class Meta:
        model = Position
        fields = ["id", "position_name", "color", "user", "category"]


class BoxChatSerializer(ModelSerializer):
    users = UserSerializer(many=True, required=False, read_only=True)
    category = CategorySerializer

    class Meta:
        model = BoxChat
        fields = ["id", "users", "category"]


class MessageSerializer(ModelSerializer):
    creator = UserSerializer
    box_chat = BoxChatSerializer

    class Meta:
        model = Message
        fields = ["id", "creator", "box_chat"]


class StepSerializer(ModelSerializer):
    user_accept = UserSerializer
    users_notification = UserSerializer(
        many=True, required=False, read_only=True)

    class Meta:
        model = Step
        fields = ["id", "step_name", "desc", "user_accept",
                  "users_notification", "status", "isAccept", "process"]


class ProcessSerializer(ModelSerializer):
    creator = UserSerializer

    class Meta:
        model = Process
        fields = ["id", "process_name", "creator", "desc", "steps"]


class WorkSerializer(ModelSerializer):
    process = ProcessSerializer
    category = CategorySerializer
    users = UserSerializer(many=True, required=False, read_only=True)

    class Meta:
        model = Work
        fields = ["id", "work_name", "desc", "status", "isProcess", "cost",
                  "start_date", "end_date", "complete_date", "users", "process", "category"]


class AdditionalWorkSerializer(ModelSerializer):
    user_accept = UserSerializer
    user_notification = UserSerializer(
        many=True, required=False)
    work = WorkSerializer

    class Meta:
        model = AdditionalWork
        fields = ["id", "additional_name", "desc", "user_accept",
                  "status", "work", "user_notification"]


class DocumentSerializer(ModelSerializer):

    class Meta:
        model = Document
        fields = '__all__'


class NotificationSerializer(ModelSerializer):

    class Meta:
        model = Notification
        fields = ["id", "content", "created_date", "type",
                  "work", "category", "project", "creator"]
