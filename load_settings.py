import sys
from google.cloud import secretmanager

client_secret_manager = secretmanager.SecretManagerServiceClient()


def download(project_number, location='settings.toml'):
    # Create GCP managed secret: https://console.cloud.google.com/security/secret-manager
    # Make sure to select upload file option, and upload your local copy of settings.toml
    name_medium_secret = "projects/{}/secrets/tap_settings_files/versions/latest".format(project_number)
    response = client_secret_manager.access_secret_version(name=name_medium_secret)
    pwd = response.payload.data.decode("UTF-8")
    with open(location, 'w') as outfile:
        outfile.write(pwd)


def upload(project_number):
    parent = client_secret_manager.secret_path(project_number, 'tap_settings_files')
    with open('settings.toml', 'r') as outfile:
        payload = outfile.read().encode("UTF-8")
        response = client_secret_manager.add_secret_version(request={"parent": parent, "payload": {"data": payload}})
        if response.state == response.State.ENABLED:
            return 'Settings.toml file was updated under GCP Secret Manager'
        else:
            return 'May have been an issue updating Settings.toml file under GCP Secret Manager'


if __name__ == "__main__":
    method = sys.argv[1]
    project_number = sys.argv[2]
    download_location = sys.argv[3]
    if str(method) == 'download' and project_number:
        download(str(project_number), download_location)
    elif str(method) == 'upload' and project_number:
        upload(str(project_number))

