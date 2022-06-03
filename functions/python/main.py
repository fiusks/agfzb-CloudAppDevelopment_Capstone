

# from ibmcloudant.cloudant_v1 import Document, CloudantV1
# from ibm_cloud_sdk_core.authenticators import IAMAuthenticator


# def getReviewsById(dict):
#     authenticator = IAMAuthenticator(dict['apiKey'])

#     service = CloudantV1(authenticator=authenticator)

#     service.set_service_url(dict['url'])

#     response = service.post_all_docs(
#         db='reviews', include_docs=True
#     )

#     mappedList = map(lambda item: {
#         "id": item['doc'].get('id'),
#         "name": item['doc']['name'],
#         "dealership": int(item['doc']['dealership']),
#         "review": item['doc']['review'],
#         "purchase": item['doc']['purchase'],
#         "purchase_date": item['doc'].get('purchase_date'),
#         "car_make": item['doc'].get('car_make'),
#         "car_model": item['doc'].get('car_model'),
#         "car_year": item['doc'].get('car_year'),
#     }, response.result['rows'])

#     filterList = filter(
#         lambda list: list['dealership'] == params['dealerId'], list(mappedList))

#     print(list(filterList))


# def postReview(dict):
#     authenticator = IAMAuthenticator(dict['apiKey'])

#     service = CloudantV1(authenticator=authenticator)

#     service.set_service_url(dict['url'])

#     if dict['review']['purchase']:
#         review = Document(
#             name=dict["review"]["name"],
#             dealership=dict["review"]["dealership"],
#             review=dict["review"]["review"],
#             purchase=dict["review"]["purchase"],
#             purchase_date=dict["review"].get("purchase_date"),
#             car_make=dict["review"]["car_make"],
#             car_model=dict["review"]["car_model"],
#             car_year=dict["review"]["car_year"]
#         )
#         response = service.post_document(
#             db='reviews', document=review
#         ).get_result()
#         return{
#             "message": "ok"
#         }
#     else:
#         review = Document(
#             name=dict["review"]["name"],
#             dealership=dict["review"]["dealership"],
#             review=dict["review"]["review"],
#             purchase=dict["review"]["purchase"],
#         )
#         response = service.post_document(
#             db='reviews', document=review
#         ).get_result()

#     return{
#         "message": "ok"
#     }
