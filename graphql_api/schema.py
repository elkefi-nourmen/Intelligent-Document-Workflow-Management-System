import graphene
from graphene_django.types import DjangoObjectType
from core.models import Document, Workflow
from django.contrib.auth.models import User

# Create GraphQL Object Types for Document, Workflow, and User models
class DocumentType(DjangoObjectType):
    class Meta:
        model = Document
        fields = '__all__'

class WorkflowType(DjangoObjectType):
    class Meta:
        model = Workflow
        fields = '__all__'

class UserType(DjangoObjectType):
    class Meta:
        model = User
        fields = '__all__'

# Define queries for fetching Documents and Workflows
class Query(graphene.ObjectType):
    all_documents = graphene.List(DocumentType)
    all_workflows = graphene.List(WorkflowType)
    all_users = graphene.List(UserType)

    # Resolve function to get all documents
    def resolve_all_documents(self, info):
        return Document.objects.all()

    # Resolve function to get all workflows
    def resolve_all_workflows(self, info):
        return Workflow.objects.all()

    # Resolve function to get all users
    def resolve_all_users(self, info):
        return User.objects.all()

# Define mutations (if needed) for creating/updating documents or workflows

class CreateDocument(graphene.Mutation):
    class Arguments:
        name = graphene.String(required=True)
        document_type = graphene.String(required=True)
        content = graphene.String(required=True)

    document = graphene.Field(DocumentType)

    def mutate(self, info, name, document_type, content):
        # Temporarily fetch the user with id=1 (superuser)
        uploaded_by_user = User.objects.get(id=1)

        # Create and save the new document
        document = Document(
            name=name,
            document_type=document_type,
            content=content,
            uploaded_by=uploaded_by_user
        )
        document.save()

        # Return the created document
        return CreateDocument(document=document)



class Mutation(graphene.ObjectType):
    create_document = CreateDocument.Field()

# Create the GraphQL schema
schema = graphene.Schema(query=Query, mutation=Mutation)