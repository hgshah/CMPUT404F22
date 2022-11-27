    // useEffect(async () => {
    //     await fetch(fetchURL, {
    //         method: 'GET',
    //         mode: 'cors',
    //         redirect: 'follow',
    //         headers: new Headers({
    //                 'Content-Type': 'application/json',
    //                 'Authorization': 'Token ' + fetchToken,
    //         })})
    //         .then((response) => {
    //             console.log(`Response: ${response} at time ${currDate}`);
    //             console.log(response.json());
    //             console.log(response.items);
    //         })
    //         .then((data) => {
    //             console.log(data)
    //             setData(data);
    //             console.log(data.json());
    //             let newD;
    //             console.log(`Data: ${newD}`);
    //         })
    //         .catch((err) => {
    //             console.log(err);
    //         });
    // }, []);