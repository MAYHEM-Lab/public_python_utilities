import React, { useState } from 'react';

function CredsForm(props) {
    //The hard brackets are "array deconstruction" operator
    const [acckey, setAcckey]  = useState("")
    const [seckey, setSeckey]  = useState("")

    const saveCreds = (evt) => {  //send creds to backend
	evt.preventDefault();
        alert(`Submitting ${acckey} and ${seckey}`)
	
        let server = "http://localhost:8118/api"
        if (process.env.REACT_APP_REMOTE) { //set this in .env file: REACT_APP_REMOTE=1
            server = "https://cjk-flasktest.herokuapp.com/api"
	}
        if (process.env.NODE_ENV !== 'development') {
            server = "https://cjk-flasktest.herokuapp.com/api"
	}
	console.log("server = "+server)
        const url = `${server}/keys`
	const bd = JSON.stringify({ "acckey":acckey, "seckey":seckey })
        fetch(url, {
            method: 'POST',
            headers: {
              'Accept': 'application/json',
              'Content-Type': 'application/json'
            },           
            body: bd     
	  }).then(response => response.json()) 
	  .then(data => {
		  console.log("SaveCreds saveCreds: Fetch Response data: ")
		  console.log(data) //don't log an object WITH a string else the conversion won't work and object will not be dumped
		  alert('response: ' + data["MESSAGE"])
	  }).catch((error) => console.log("SaveCreds saveCreds: Fetch Failure: "+ error))
    }

    //See this example on Creating Custom Hooks at  https://rangle.io/blog/simplifying-controlled-inputs-with-hooks/ to preclude the need to add a function handleChange for each onChange event
    return (
      <div>
      <h3>Server: {process.env.NODE_ENV} </h3>
      <form onSubmit={saveCreds}>
        <label>
          Access Key:
          <input 
	    type="text" 
	    value={acckey} 
	    name="acckey" 
	    onChange={e => setAcckey(e.target.value)} />
        </label>
        <label>
          Secret Key:
          <input 
	    type="text" 
	    value={seckey} 
	    name="seckey" 
	    onChange={e => setSeckey(e.target.value)} />
        </label>
        <input type="submit" value="Submit" />
      </form>
      </div>
    )
}
export default CredsForm;
