import graphene
from graphene_django.types import DjangoObjectType
from django.contrib.auth.models import User
from core.models import Document, Workflow


# Define UserType for handling User objects
class UserType(DjangoObjectType):
    class Meta:
        model = User


# Define DocumentType for handling Document objects
class DocumentType(DjangoObjectType):
    class Meta:
        model = Document
        fields = ("id", "title", "document_type", "file", "status", "uploaded_by", "uploaded_at", "updated_at")


# Define WorkflowType for handling Workflow objects
class WorkflowType(DjangoObjectType):
    class Meta:
        model = Workflow

    assigned_to = graphene.Field(UserType)  
    document = graphene.Field(DocumentType)  


# Query to fetch data
class Query(graphene.ObjectType):
    workflows_with_document_and_user = graphene.List(WorkflowType)
    all_documents = graphene.List(DocumentType)
    document_by_id = graphene.Field(DocumentType, document_id=graphene.ID(required=True))

    def resolve_workflows_with_document_and_user(self, info):
        return Workflow.objects.select_related('assigned_to', 'document').all()

    def resolve_all_documents(self, info):
        return Document.objects.all()

    def resolve_document_by_id(self, info, document_id):
        return Document.objects.get(pk=document_id)


# Mutations for Document operations
class CreateDocument(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        title = graphene.String(required=True)
        document_type = graphene.String(required=True)
        file = graphene.String(required=True)

    def mutate(self, info, title, document_type, file):
        user = info.context.user
        if user.is_anonymous:
            raise Exception("You must be logged in to upload a document.")

        document = Document(
            title=title,
            document_type=document_type,
            file=file,
            uploaded_by=user,
        )
        document.save()

        return CreateDocument(document=document)


class UpdateDocumentStatus(graphene.Mutation):
    document = graphene.Field(DocumentType)

    class Arguments:
        document_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, document_id, status):
        user = info.context.user
        if not user.groups.filter(name='Manager').exists():
            raise Exception("You do not have permission to update document status.")

        document = Document.objects.get(pk=document_id)
        document.status = status
        document.save()

        return UpdateDocumentStatus(document=document)


class DeleteDocument(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        document_id = graphene.ID(required=True)

    def mutate(self, info, document_id):
        user = info.context.user
        if not user.groups.filter(name='Manager').exists():
            raise Exception("You do not have permission to delete documents.")

        document = Document.objects.get(pk=document_id)
        document.delete()

        return DeleteDocument(success=True)


# Mutations for Workflow operations
class CreateWorkflow(graphene.Mutation):
    workflow = graphene.Field(WorkflowType)

    class Arguments:
        document_id = graphene.ID(required=True)
        assigned_to_id = graphene.ID(required=True)
        current_step = graphene.String(required=True)

    def mutate(self, info, document_id, assigned_to_id, current_step):
        user = info.context.user
        if not user.groups.filter(name='Manager').exists():
            raise Exception("You do not have permission to create workflows.")

        document = Document.objects.get(pk=document_id)
        assigned_to = User.objects.get(pk=assigned_to_id)

        workflow = Workflow(
            document=document, assigned_to=assigned_to, current_step=current_step
        )
        workflow.save()

        return CreateWorkflow(workflow=workflow)


class UpdateWorkflowStatus(graphene.Mutation):
    workflow = graphene.Field(WorkflowType)

    class Arguments:
        workflow_id = graphene.ID(required=True)
        status = graphene.String(required=True)

    def mutate(self, info, workflow_id, status):
        user = info.context.user
        if not user.groups.filter(name='Manager').exists():
            raise Exception("You do not have permission to update workflow status.")

        workflow = Workflow.objects.get(pk=workflow_id)
        workflow.status = status
        workflow.save()

        return UpdateWorkflowStatus(workflow=workflow)


class DeleteWorkflow(graphene.Mutation):
    success = graphene.Boolean()

    class Arguments:
        workflow_id = graphene.ID(required=True)

    def mutate(self, info, workflow_id):
        user = info.context.user
        if not user.groups.filter(name='Manager').exists():
            raise Exception("You do not have permission to delete workflows.")

        workflow = Workflow.objects.get(pk=workflow_id)
        workflow.delete()

        return DeleteWorkflow(success=True)


# Define the Schema for GraphQL
class Mutation(graphene.ObjectType):
    create_document = CreateDocument.Field()
    update_document_status = UpdateDocumentStatus.Field()
    delete_document = DeleteDocument.Field()

    create_workflow = CreateWorkflow.Field()
    update_workflow_status = UpdateWorkflowStatus.Field()
    delete_workflow = DeleteWorkflow.Field()


# Define the schema with Query and Mutation types
schema = graphene.Schema(query=Query, mutation=Mutation)
