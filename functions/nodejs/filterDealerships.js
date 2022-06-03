/**
 * Get all dealerships
 */

// const { CloudantV1 } = require("@ibm-cloud/cloudant");
// const { IamAuthenticator } = require("ibm-cloud-sdk-core");

// async function main(params) {
//   const authenticator = new IamAuthenticator({
//     apikey: params.apiKey,
//   });
//   const cloudant = CloudantV1.newInstance({
//     authenticator: authenticator,
//   });
//   cloudant.setServiceUrl(params.url);
//   const dbName = "dealerships";

//   try {
//     const allFromDB = await cloudant.postAllDocs({
//       db: dbName,
//       includeDocs: true,
//     });
//     const listAll = allFromDB.result.rows.map((dealer) => {
//       const {
//         doc: { id, city, state, st, address, zip, lat, long, full_name },
//       } = dealer;
//       return {
//         id,
//         city,
//         state,
//         st,
//         address,
//         zip,
//         lat,
//         long,
//         full_name,
//       };
//     });

//     function getFilteredList(filterName, value) {
//       const appliedFilter = listAll.filter(
//         (dealer) => String(dealer[filterName]) === String(value)
//       );
//       return appliedFilter[0];
//     }

//     filteredList = {};
//     if (params?.state) {
//       filteredList = getFilteredList("st", params.state);
//     } else if (params.dealerId) {
//       filteredList = getFilteredList("id", params.dealerId);
//     } else {
//       filteredList = listAll;
//     }

//     if (!Object.keys(filteredList).length) {
//       console.log("entrei");
//       return {
//         error: "No match",
//       };
//     }
//     const result = { dealership: filteredList };
//     console.log(filteredList);
//     return {
//       result,
//     };
//   } catch (error) {
//     return error;
//   }
// }
