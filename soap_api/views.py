import os
import base64
from django.conf import settings
from django.views.decorators.csrf import csrf_exempt
from spyne import Application, rpc, ServiceBase, Unicode, Integer, ComplexModel, Byte
from spyne.protocol.soap import Soap11
from spyne.server.django import DjangoApplication
from django.contrib.auth.models import User
from core.models import Document


class UserImportInput(ComplexModel):
    username = Unicode
    password = Unicode
    first_name = Unicode
    last_name = Unicode
    email = Unicode


class UserExportOutput(ComplexModel):
    user_id = Integer
    username = Unicode
    first_name = Unicode
    last_name = Unicode
    email = Unicode


class DocumentUploadInput(ComplexModel):
    title = Unicode
    document_type = Unicode
    file = Unicode
    user_id = Integer


# ComplexType for document status
class DocumentStatusOutput(ComplexModel):
    status = Unicode


class CustomService(ServiceBase):
    """
    SOAP Service with methods for importing/exporting users, uploading documents, and getting document statuses.
    """

    @rpc(UserImportInput, _returns=Unicode)
    def import_user(ctx, user_input):
        """Creates a new user with the provided details."""
        try:
            user = User.objects.create_user(
                username=user_input.username,
                password=user_input.password,
                first_name=user_input.first_name,
                last_name=user_input.last_name,
                email=user_input.email
            )
            return f"User {user.username} created successfully with ID {user.id}"
        except Exception as e:
            return f"Error creating user: {str(e)}"

    @rpc(Integer, _returns=UserExportOutput)
    def export_user(ctx, user_id):
        """Fetches the details of a user by their ID."""
        try:
            user = User.objects.get(id=user_id)
            return UserExportOutput(
                user_id=user.id,
                username=user.username,
                first_name=user.first_name,
                last_name=user.last_name,
                email=user.email
            )
        except User.DoesNotExist:
            raise ValueError("User not found")

    
    @rpc(DocumentUploadInput, _returns=Unicode)
    def upload_document(ctx, doc_input):
            """
            Crée un document, l'associe à un utilisateur et enregistre le fichier à partir d'un chemin local.
            """
            try:
                # Vérifier si le fichier existe au chemin donné
                if not os.path.exists(doc_input.file):
                    return "File not found at the specified path"

                #nom du fichier
                file_name = f"{doc_input.title}_{doc_input.user_id}.pdf"

                # Sauvegarder le fichier dans MEDIA_ROOT
                destination_path = os.path.join(settings.MEDIA_ROOT, "documents", file_name)

                # Créer le dossier s'il n'existe pas déjà
                os.makedirs(os.path.dirname(destination_path), exist_ok=True)

                # Copier le fichier depuis son chemin local vers le dossier de destination
                with open(doc_input.file, "rb") as src_file:
                    with open(destination_path, "wb") as dest_file:
                        dest_file.write(src_file.read())

                # Créer un document dans la base 
                user = User.objects.get(id=doc_input.user_id)
                document = Document.objects.create(
                    title=doc_input.title,
                    document_type=doc_input.document_type,  
                    uploaded_by=user,  
                    file=f"documents/{file_name}"  #Chemin relatif pour la base
                )

                return f"Document '{doc_input.title}' uploaded successfully"
            except User.DoesNotExist:
                return "User not found"
            except Exception as e:
                return f"An error occurred: {str(e)}"

    @rpc(Integer, _returns=DocumentStatusOutput)
    def get_document_status(ctx, document_id):
        """Fetches the status of a document by its ID."""
        try:
            document = Document.objects.get(id=document_id)
            return DocumentStatusOutput(status=document.status)
        except Document.DoesNotExist:
            raise ValueError("Document not found")


soap_app = Application(
    [CustomService],
    tns='django.soap.service',
    in_protocol=Soap11(),
    out_protocol=Soap11()
)

soap_application = csrf_exempt(DjangoApplication(soap_app))