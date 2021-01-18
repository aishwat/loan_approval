const test = async (n) => {
    const axios = require('axios');
    var data = JSON.stringify({
        "customerID": 100000,
        "dob": "01/01/1977",
        "income": 25000,
        "bureauScore": 700,
        "applicationScore": 750,
        "maxDelL12M": 0,
        "allowedFoir": 60,
        "existingEMI": 2000,
        "loanTenure": 24,
        "currentAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037",
        "bureauAddress": "15 2nd cross vagdevi layout Marathahalli Bangalore Karnataka 560037"
    });

    let url = 'http://localhost:8000/status'
    let promises = []
    for (let i = 0; i < n; i++) {
        promises.push(axios.post(url, data).then(resp => {
            return resp.data
        }))
    }
    let t1 = Date.now()
    let res = await axios.all(promises)
    let t2 = Date.now()
    console.log(`calls:${n}, time:${t2-t1}, avg_time:${(t2-t1)/n}`)


}
test(10)
test(100)
test(1000)