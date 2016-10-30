from cloudfoundry_client.client import CloudFoundryClient

class CloudFoundryUtil:
    
    def __init__(self, target_endpoint, username, password):
        client = CloudFoundryClient(target_endpoint, skip_verification=False)
        client.init_with_user_credentials(username, password)
        self.client = client
    
    def list_spaces(self):
        s = []
        for organization in self.client.organizations:
            for space in organization.spaces():
                s.append ((
                    organization['entity']['name'], 
                    space['entity']['name'],
                    space['metadata']['guid']
                    ))
        return s

    def get_organization(self, organization_name):
        for organization in self.client.organizations:
            if organization['entity']['name'] == organization_name:
                return organization
        raise ValueError("Oranization '{0}' not found.".format(organization_name))

    def get_space(self, organization_name, space_name):
        organization = self.get_organization(organization_name)
        for space in organization.spaces():
            if space['entity']['name'] == space_name:
                return space
        raise ValueError("Space '{0}' not found.".format(space_name))

    def get_space_guid(self, organization_name, space_name):
        space = self.get_space(organization_name, space_name)
        if space:
            return space['metadata']['guid']
        else:
            return None

    def search_plans(self, string):
        for sp in self.client.service_plans.list():
            if string in json.dumps(sp).lower():
                return sp
        return None

    def create_service_keys(self, service_instance, credentials_name = 'Credentials-1'):
        url = target_endpoint + '/v2/service_keys'
        data = dict(
                  service_instance_guid = service_instance['metadata']['guid'],
                  name = credentials_name
               )
        response = service_instance.client.post(url, json=data)
        return response

    def get_service_keys(self, service_name):
        return self.client.service_instances.get_first(name=service_name)
    
    def get_service_credential(self, service_name, credential_name):
        service_instance = self.get_service_instance(service_name)
        return list(service_instance.service_keys())[0]['entity']['credentials'][credential_name]
    
    def delete_service_keys(self, service_keys_instance):
        url = target_endpoint + '/v2/service_keys/' + service_keys_instance['metadata']['guid']
        response = service_keys_instance.client.delete(url)
        print(response.text)
        return response

    def delete_service(self, service_instance_name, force=False):
        si = self.get_service_instance(service_instance_name)
            
        if force == True and si:
            for k in si.service_keys():
                self.delete_service_keys(k)
        self.client.service_instances.remove(si['metadata']['guid'])
        
    def get_service_instance(self, name):
        return self.client.service_instances.get_first(name=name)
        
    def get_service_plan(self, service_guid):
        return self.client.service_plans.get_first(service_guid=service_guid)
    
    def get_service_plan_id(self, service_plan):
        return service_plan['metadata']['guid']
    
    def create_service_instance(self, organization_name, space_name, service_plan_guid, service_name_to_create, create_default_credentials = True):
        space_guid = self.get_space_guid(organization_name, space_name)
        service_plan = self.get_service_plan(service_plan_guid)
        service_plan_id = self.get_service_plan_id(service_plan)
        service_instance = self.client.service_instances.create(
            space_guid, 
            service_name_to_create,
            service_plan_id
        )
        
        if create_default_credentials:
            resp = self.create_service_keys(service_instance)
            resp.raise_for_status()
