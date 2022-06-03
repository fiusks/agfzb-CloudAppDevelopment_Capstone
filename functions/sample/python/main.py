#
#
# main() will be run when you invoke this action
#
# @param Cloud Functions actions accept a single parameter, which must be a JSON object.
#
# @return The output of this action, which must be a JSON object.
#
#

from ibmcloudant.cloudant_v1 import Document, CloudantV1
from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


params = {}
params['review'] = {"apiKey": "NY3lB4ceEKimktL5qQ-H1y7jLVmw_uVrwzedWdV2PwOS",
                    "url": "https://apikey-v2-2inqni6tqfn1mzqxhlrve4q67tbch3oeyr6dwaif20zr:b6e55f116e94747c60d841fde09ece41@db29386c-4db3-478f-bbcd-f0469763ece3-bluemix.cloudantnosqldb.appdomain.cloud",
                    "name": "Coding Partners",
                    "dealership": 45,
                    "review": "It is awesome",
                    "purchase": True,
                    "car_make": "Fordizera",
                    "car_model": "Mustang",
                    "car_year": "2015",
                    }


def main(dict):
    authenticator = IAMAuthenticator(dict['apiKey'])

    service = CloudantV1(authenticator=authenticator)

    service.set_service_url(dict['url'])

    response = service.post_all_docs(
        db='reviews', include_docs=True
    )

    mappedList = map(lambda item: {
        "id": item['doc'].get('id'),
        "name": item['doc']['name'],
        "dealership": int(item['doc']['dealership']),
        "review": item['doc']['review'],
        "purchase": item['doc']['purchase'],
        "purchase_date": item['doc'].get('purchase_date'),
        "car_make": item['doc'].get('car_make'),
        "car_model": item['doc'].get('car_model'),
        "car_year": item['doc'].get('car_year'),
    }, response.result['rows'])

    filterList = filter(
        lambda list: list['dealership'] == params['dealerId'], list(mappedList))
    # result = {"entries": list(filterList)}
    print(list(filterList))

    # if len(result["entries"]) == 0:

    #     return {"message": "No match"}
    # else:
    #     return result


def main(dict):
    authenticator = IAMAuthenticator(dict['apiKey'])

    service = CloudantV1(authenticator=authenticator)

    service.set_service_url(dict['url'])

    if dict['review']['purchase']:
        review = Document(
            name=dict["review"]["name"],
            dealership=dict["review"]["dealership"],
            review=dict["review"]["review"],
            purchase=dict["review"]["purchase"],
            purchase_date=dict["review"].get("purchase_date"),
            car_make=dict["review"]["car_make"],
            car_model=dict["review"]["car_model"],
            car_year=dict["review"]["car_year"]
        )
        response = service.post_document(
            db='reviews', document=review
        ).get_result()
        return{
            "message": "ok"
        }
    else:
        review = Document(
            name=dict["review"]["name"],
            dealership=dict["review"]["dealership"],
            review=dict["review"]["review"],
            purchase=dict["review"]["purchase"],
        )
        response = service.post_document(
            db='reviews', document=review
        ).get_result()

    return{
        "message": "ok"
    }
