import os
import streamlit as st
from PIL import Image
from google.cloud import storage
import requests


 

def file_selector(folder_path='.'):
    filenames = os.listdir(folder_path)
    selected_filename = st.selectbox('Select a file', filenames)
    return os.path.join(folder_path, selected_filename)

@st.cache
def load_image(image_file):
    img = Image.open(image_file)
    return img 

if __name__ == '__main__':
    # Select a file
    st.markdown("""# Transform any image into a monet-painting
    ##Upload an image
    """)
    current_directory = os.getcwd()
    final_directory = os.path.join(current_directory, r'tempDir')
    if not os.path.exists(final_directory):
        os.makedirs(final_directory)
    
    uploaded_file = st.file_uploader("Upload Files",type=['png','jpg','jpeg'])
    
    if uploaded_file is not None:
        file_details = {"FileName":uploaded_file.name,"FileType":uploaded_file.type,"FileSize":uploaded_file.size}
        filename = file_details['FileName']
        
        st.write(file_details)   
        img = load_image(uploaded_file)
        st.image(img, caption = "Uploaded Image")
        with open(os.path.join("tempDir",uploaded_file.name),"wb") as f: 
            f.write(uploaded_file.getbuffer())         
            st.success("Saved File")    
        filepath = (os.path.join("tempDir",uploaded_file.name))
        st.write(filepath)
        
        

        
        # DISPLAYING THE UPLOADED IMAGE
        
        
        
        
                
        
        
        
        
        #st.write(os.path.basename(filepath))
        # def find_files(filename, search_path):
        #     result = []

        #     # Walking top-down from the root
        #     for root, dir, files in os.walk(search_path):
        #         if filename in files:
        #             result.append(os.path.join(root, filename))
        #     return result
        # st.write("tes tes tes")
        # st.write(find_files(filepath,"C:"))
        
    
    # if st.checkbox('Select a file in current directory'):
    #     folder_path = '.'
    #     if st.checkbox('Change directory'):
    #         folder_path = st.text_input('Enter folder path', '.')
    #     filepath = file_selector(folder_path=folder_path)
    #     #st.write('You selected `%s`' % filepath)
        
     # if filepath.endswith("jpg") or filepath.endswith("png"):
        #     image = Image.open(filepath)
        #     st.image(image, caption=st.markdown('''#Uploaded File'''), use_column_width=False)]]
            
       
############# GOOGLE CLOUD PLATFORM #########################################
        
        os.environ['GOOGLE_APPLICATION_CREDENTIALS'] = 'google-credentials.json'

        storage_client = storage.Client()

        bucket_name = 'bucket-monet-gan'


        #Accessing the bucket
        
        my_bucket = storage_client.get_bucket(bucket_name)

        #Uploading files
        if filepath.endswith("jpg") or filepath.endswith("jpeg") or filepath.endswith("png"):
            def upload_to_bucket(blob_name, file_path, bucket_name):
                try:
                    bucket = storage_client.get_bucket(bucket_name)
                    blob = bucket.blob(blob_name)
                    blob.upload_from_filename(file_path)
                    return True

                except Exception as e:
                    print(e)
                    return False
        
               
            
            filename_upload = f'frontend_upload_images./{filepath}'
            

            #calling the upload function as a condition to then downloading file from bucket 
            if upload_to_bucket(filename_upload,filepath,bucket_name):
                def download_from_bucket(blob_name, file_path, bucket_name):
                    try:
                        bucket = storage_client.get_bucket(bucket_name)
                        blob = bucket.blob(blob_name)
                        with open(file_path, 'wb') as f:
                            storage_client.download_blob_to_file(blob, f)
                        return True

                    except Exception as e:
                        print(e)
                        return False
                    
                #calling the download function
                folder_name = 'frontend_download_images'
                filename_download = filepath
                download_from_bucket(f'{folder_name}/{filepath}',os.getcwd(),bucket_name)
                downloaded_image_path = uploaded_file.name
                
                image2 = Image.open(downloaded_image_path)
                st.image(image2, caption=st.markdown('''#Downloaded Image'''), use_column_width=False)
        
        
        
            
            
            
        