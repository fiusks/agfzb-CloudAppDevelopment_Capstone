/**
 * Get all dealerships
 */

const { CloudantV1 } = require("@ibm-cloud/cloudant");
const { IamAuthenticator } = require("ibm-cloud-sdk-core");
params = {
  apiKey: "NY3lB4ceEKimktL5qQ-H1y7jLVmw_uVrwzedWdV2PwOS",
  url: "https://apikey-v2-2inqni6tqfn1mzqxhlrve4q67tbch3oeyr6dwaif20zr:b6e55f116e94747c60d841fde09ece41@db29386c-4db3-478f-bbcd-f0469763ece3-bluemix.cloudantnosqldb.appdomain.cloud",
  st: "CA",
};
async function main(params) {
  const authenticator = new IamAuthenticator({
    apikey: params.apiKey,
  });
  const cloudant = CloudantV1.newInstance({
    authenticator: authenticator,
  });
  cloudant.setServiceUrl(params.url);
  const dbName = "dealerships";

  try {
    const allFromDB = await cloudant.postAllDocs({
      db: dbName,
      includeDocs: true,
    });
    const listAll = allFromDB.result.rows.map((dealer) => {
      const {
        doc: { id, city, state, st, address, zip, lat, long, full_name },
      } = dealer;
      return {
        id,
        city,
        state,
        st,
        address,
        zip,
        lat,
        long,
        full_name,
      };
    });
    if (params.state) {
      const filteredList = listAll.filter(
        (dealer) => dealer.st === params.state
      );
      return {
        dealerships: filteredList,
      };
    } else {
      return {
        dealerships: listAll,
      };
    }
  } catch (error) {
    return error;
  }
}

main(params);
