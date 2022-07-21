from django.http import Http404
from rest_framework.response import Response
from rest_framework.decorators import action
from rest_framework.parsers import MultiPartParser
from rest_framework import viewsets, permissions, status, generics
from .models import (AdditionalWork, BoxChat, Category, Department, Document, Message, Position, Process, Project, Stage, Step, User, Work
                     )
from .serializers import (
    AdditionalWorkSerializer,
    BoxChatSerializer,
    CategorySerializer,
    DepartmentSerializer,
    DocumentSerializer,
    MessageSerializer,
    MyTokenObtainPairSerializer,
    PositionSerializer,
    ProcessSerializer,
    ProjectSerializer,
    StageSerializer,
    StepSerializer,
    UserSerializer,
    WorkSerializer)
from django.conf import settings
from rest_framework.views import APIView
from rest_framework_simplejwt.views import TokenObtainPairView
from django.core.mail import BadHeaderError, send_mail
from django.http import HttpResponse, HttpResponseRedirect


class UserViewSet(viewsets.ViewSet, generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView):
    queryset = User.objects.filter(is_active=True)
    serializer_class = UserSerializer
    parser_classes = [MultiPartParser]

    def get_permissions(self):
        if self.action == 'get_current_user':
            return [permissions.IsAuthenticated()]
        return [permissions.AllowAny()]

    @action(methods=['get'], detail=False, url_path='current-user')
    def get_current_user(seft, request):
        return Response(seft.serializer_class(request.user).data, status=status.HTTP_200_OK)

    def list(self, request):
        queryset = User.objects.all()
        serializer = UserSerializer(queryset, many=True)
        return Response(data={"listUsers": serializer.data})


class AuthInfo(APIView):
    def get(seft, request):
        return Response(settings.OAUTH2_INFO, status=status.HTTP_200_OK)


class MyTokenObtainPairView(TokenObtainPairView):
    serializer_class = MyTokenObtainPairSerializer


class DepartmentViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Department.objects.filter(active=True)
    serializer_class = DepartmentSerializer
    permission_classes = [permissions.IsAuthenticated]


class ProjectViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Project.objects.filter(active=True)
    serializer_class = ProjectSerializer

    def list(self, request):
        projects = Project.objects.filter(active=True)
        department_id = request.query_params.get('department_id')
        if department_id is not None:
            projects = projects.filter(department_id=department_id)

        user_id = request.query_params.get('user_id')
        if user_id is not None:
            projects = projects.filter(users__id=user_id)

        serializer = ProjectSerializer(projects, many=True)
        return Response(data={"listProjects": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='categories')
    def get_categories(self, request, pk):
        categories = []
        stages = self.get_object().stages.filter(active=True)

        if stages is not None:
            for stage in stages:
                categories += stage.categories.filter(active=True)

        return Response(data={"categories": CategorySerializer(categories, many=True).data}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=True, url_path='works')
    def get_works(self, request, pk):
        categories = []
        works = []
        stages = self.get_object().stages.filter(active=True)

        for stage in stages:
            categories += stage.categories.filter(active=True)

        for category in categories:
            works += category.works.filter(active=True)

        return Response(data={"works": WorkSerializer(works, many=True).data}, status=status.HTTP_200_OK)


class StageViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Stage.objects.filter(active=True)
    serializer_class = StageSerializer

    def list(self, request):
        stages = Stage.objects.filter(active=True).order_by("-pos")
        project_id = request.query_params.get('project_id')
        if project_id is not None:
            stages = stages.filter(project_id=project_id)

        serializer = StageSerializer(stages, many=True)
        return Response(data={"listStages": serializer.data}, status=status.HTTP_200_OK)


class CategoryViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Category.objects.filter(active=True)
    serializer_class = CategorySerializer

    def list(self, request):
        categories = Category.objects.filter(active=True)
        stage_id = request.query_params.get('stage_id')
        if stage_id is not None:
            categories = categories.filter(stage_id=stage_id)
        serializer = CategorySerializer(categories, many=True)

        return Response(data={"listCategories": serializer.data}, status=status.HTTP_200_OK)


class PositionViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Position.objects.filter(active=True)
    serializer_class = PositionSerializer

    def list(self, request):
        positions = Position.objects.filter(active=True)
        cate_id = request.query_params.get('cate_id')
        if cate_id is not None:
            positions = positions.filter(category_id=cate_id)

        position_name = request.query_params.get('position_name')
        if position_name is not None:
            positions = positions.filter(position_name=position_name)
        user_id = request.query_params.get('user_id')
        if user_id is not None:
            positions = positions.filter(user_id=user_id)
        serializer = PositionSerializer(positions, many=True)
        return Response(data={"listPositions": serializer.data}, status=status.HTTP_200_OK)


class BoxChatViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = BoxChat.objects.filter(active=True)
    serializer_class = BoxChatSerializer

    def list(self, request):
        boxs = BoxChat.objects.filter(active=True)
        cate_id = request.query_params.get('cate_id')
        if cate_id is not None:
            boxs = boxs.filter(category_id=cate_id)

        serializer = BoxChatSerializer(boxs, many=True)
        return Response(data={"listBoxs": serializer.data}, status=status.HTTP_200_OK)


class MessageViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Message.objects.filter(active=True)
    serializer_class = MessageSerializer

    def list(self, request):
        messages = Message.objects.filter(active=True)
        box_id = request.query_params.get('box_id')
        if box_id is not None:
            messages = messages.filter(box_chat_id=box_id)

        serializer = MessageSerializer(messages, many=True)
        return Response(data={"listBoxs": serializer.data}, status=status.HTTP_200_OK)


class ProcessViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Process.objects.filter(active=True)
    serializer_class = ProcessSerializer


class StepViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Step.objects.filter(active=True)
    serializer_class = StepSerializer

    def list(self, request):
        steps = Step.objects.filter(active=True)
        process_id = request.query_params.get('process_id')
        if process_id is not None:
            steps = steps.filter(process_id=process_id)
        return Response(data={"listSteps": StepSerializer(steps, many=True).data}, status=status.HTTP_200_OK)


class WorkViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Work.objects.filter(active=True)
    serializer_class = WorkSerializer

    def list(self, request):
        works = Work.objects.filter(active=True)
        cate_id = request.query_params.get('cate_id')
        if cate_id is not None:
            works = works.filter(category_id=cate_id)

        user_id = request.query_params.get('user_id')
        if user_id is not None:
            works = works.filter(users__id=user_id)

        serializer = WorkSerializer(works, many=True)
        return Response(data={"listWorks": serializer.data}, status=status.HTTP_200_OK)

    @action(methods=['post'], detail=True, url_path='add_users')
    def add_user(self, request, pk):
        try:
            work = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            users = request.data.get('users')
            if users is not None:
                for user in users:
                    work.users.add(user)
                return Response(self.serializer_class(work).data, status=status.HTTP_201_CREATED)

        return Response(status=status.HTTP_404_NOT_FOUND)

    @action(methods=['post'], detail=True, url_path='delete_users')
    def delete_user(self, request, pk):
        try:
            work = self.get_object()
        except Http404:
            return Response(status=status.HTTP_404_NOT_FOUND)
        else:
            users = request.data.get('users')
            if users is not None:
                for user in users:
                    work.users.remove(user)
                return Response(self.serializer_class(work).data, status=status.HTTP_204_NO_CONTENT)

        return Response(status=status.HTTP_404_NOT_FOUND)


class AdditionalWorkViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = AdditionalWork.objects.filter(active=True)
    serializer_class = AdditionalWorkSerializer

    def list(self, request):
        additionalWorks = AdditionalWork.objects.filter(active=True)
        work_id = request.query_params.get('work_id')
        if work_id is not None:
            additionalWorks = additionalWorks.filter(work_id=work_id)

        serializer = AdditionalWorkSerializer(additionalWorks, many=True)
        return Response(data={"lists": serializer.data}, status=status.HTTP_200_OK)


class DocumentViewSet(viewsets.ViewSet,  generics.ListAPIView, generics.CreateAPIView, generics.UpdateAPIView, generics.RetrieveAPIView, generics.DestroyAPIView):
    queryset = Document.objects.filter(active=True)
    serializer_class = DocumentSerializer

    def list(self, request):
        documents = Document.objects.filter(active=True)
        work_id = request.query_params.get('work_id')
        if work_id is not None:
            documents = documents.filter(work_id=work_id)
        creator = request.query_params.get('creator')
        if creator is not None:
            documents = documents.filter(creator=creator)
        process_id = request.query_params.get('process_id')
        if process_id is not None:
            documents = documents.filter(process_id=process_id)

        serializer = DocumentSerializer(documents, many=True)
        return Response(data={"listDocuments": serializer.data}, status=status.HTTP_200_OK)
