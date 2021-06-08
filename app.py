import os, uuid, sys
from azure.storage.blob import BlockBlobService, PublicAccess



def run_sample():
    try:
        # Create the BlockBlockService that is used to call the Blob service for the storage account
        block_blob_service = BlockBlobService(account_name='rxa5014storage', account_key='Apk1DlIhjJKIlodD/KDtAryxBYORJ48bfuLL05azxOa0J5r0Jesaa7Wt3XRwZdpCDePGrE0WWFk1rDapwI74UA==')

        # Create a container called 'quickstartblobs'.
        container_name ='pictures'
        block_blob_service.create_container(container_name)

        # Set the permission so the blobs are public.
        block_blob_service.set_container_acl(container_name, public_access=PublicAccess.Container)

        # Create a file in Documents to test the upload and download.
        local_path=os.path.abspath(os.path.curdir)
        local_file_name ="pic1.jpg"
        full_path_to_file =os.path.join(local_path, local_file_name)

        # Write text to the file.
        #file = open(full_path_to_file,  'w')
        #file.write("Hello, World!")
        #file.close()

        print("Temp file = " + full_path_to_file)
        print("\nUploading to Blob storage as blob" + local_file_name)

        # Upload the created file, use local_file_name for the blob name
        block_blob_service.create_blob_from_path(container_name, local_file_name, full_path_to_file)

        # List the blobs in the container
        print("\nList blobs in the container")
        generator = block_blob_service.list_blobs(container_name)
        for blob in generator:
            print("\t Blob name: " + blob.name)

        
        
    except Exception as e:
        print(e)


# Main method.
if __name__ == '__main__':
    run_sample()



