import React, {useRef, useState} from "react";
import Button from 'react-bootstrap/Button';
import Form from 'react-bootstrap/Form';


const LoginPage = () => {

    const usernameRef: React.MutableRefObject<HTMLInputElement | null> = useRef(null);
    const passwordRef: React.MutableRefObject<HTMLInputElement | null>  = useRef(null);

    const [credentialsError, setCredentialsError] = useState("");

    async function checkCredentials(){
        console.log(123)
        if(!usernameRef?.current?.value){
            setCredentialsError("No username provided")
            return
        }

        if(!passwordRef?.current?.value){
            setCredentialsError("No password provided")
            return
        }

        const requestOptions = {
            method: 'POST',
            mode: 'no-cors', // Set the request's mode to 'no-cors'
            headers: { 'Content-Type': 'application/json' },
            body: JSON.stringify({
                "username": usernameRef.current?.value,
                "password": passwordRef.current?.value,
            })
        };
        console.log(requestOptions.body);
        const response: any = await fetch("http://localhost:8000/api/user/auth/token/", requestOptions)
            .then(res => {
                return res.json()
            })
        console.log(response);
    }

    return (
        <div className='flex flex-col'>
        <input type="text" placeholder="username" ref={usernameRef}/>
        <input type="password" placeholder="password" ref={passwordRef}/>
            <button onClick={checkCredentials}>Submit</button>
            {credentialsError ? credentialsError : ''}
        </div>
    )
}
export {LoginPage}
