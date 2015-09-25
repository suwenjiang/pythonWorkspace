import urllib, json, time, traceback

#change to your server URL
base_url = 'http://192.168.100.202:6080/arcgis/rest/'

def openURL(url,params=None):
    try:
        request_params = {'f':'pjson'}
        if params:
            request_params.update(params)
        encodedParams = urllib.urlencode(request_params)
        request = urllib.urlopen(url,encodedParams)
        response = request.read()
        json_response = json.loads(response)
        return json_response
    except:
        print response
        print traceback.format_exc()

rest_info = openURL(base_url)


def launchDescriptionServices(rest_info, nb_of_services):
    val = 0
    description_time_mean = 0.0
    print len(rest_info['services'])
    for service in rest_info['services']:
        if val >= nb_of_services:
            break
        val +=1
        service_url = '{0}/services/{1}/MapServer'.format(base_url,service['name'])
        start_time = time.time()
        service_json = openURL(service_url)
        end_time = time.time()

        elapsed = end_time - start_time
        description_time_mean = description_time_mean + elapsed
        print val, elapsed

    if val != 0:
        description_time_mean = description_time_mean / val

    print "Service description mean " + str(description_time_mean)


# first launch, cache the services

print("Cache 1st 260 services")
launchDescriptionServices(rest_info,260)

print("calculate the mean for 400 services")
launchDescriptionServices(rest_info,260)

#
# print("Cache all services")
# launchDescriptionServices(rest_info,1000)
#
# print("calculate the mean for all services")
# launchDescriptionServices(rest_info,1000)








