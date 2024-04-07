import { Button, Form } from "react-bootstrap"
import { OffCanvas } from "../../components/OffCanvas"
import { MutableRefObject, useRef, useState } from "react"
import { request } from "../../utils/request";

export const AddUser = () => {
    

  const [validated, setValidated] = useState(false);

    const usernameRef = useRef<MutableRefObject<HTMLInputElement>>();
    const passwordRef = useRef<MutableRefObject<HTMLInputElement>>();
    const firstnameRef = useRef<MutableRefObject<HTMLInputElement>>();
    const lastnameRef = useRef<MutableRefObject<HTMLInputElement>>();
    const imageRef = useRef<MutableRefObject<HTMLInputElement>>();
    
    const errorRef = useRef<MutableRefObject<HTMLDivElement>>();

  const handleSubmit = (event) => {
    const form = event.currentTarget;
      event.preventDefault();
      event.stopPropagation();
    setValidated(true)

    if(
        !usernameRef?.current || !passwordRef?.current || !firstnameRef?.current
        || !lastnameRef?.current || !imageRef?.current
    ){console.log("no values");return}
    if(
        !usernameRef.current?.value || !passwordRef.current?.value || !firstnameRef.current?.value
        || !lastnameRef.current?.value || !imageRef.current?.value
    ){console.log("no render");return}

    const file = imageRef.current.files[0];
    if (!file) { return}
    const reader = new FileReader();
    reader.onloadend = function () {
        // Convert ArrayBuffer to Hex string
    const buffer = reader.result;
    const view = new DataView(buffer);
    let hexStr = '';
    for (let i = 0; i < view.byteLength; i += 1) {
    const byte = view.getUint8(i).toString(16);
    hexStr += (byte.length === 1 ? '0' : '') + byte;
    

    request({
        url: "user/", method: "POST",
        body: JSON.stringify({
            username: usernameRef?.current.value,
            password: passwordRef?.current.value,
            first_name: firstnameRef.current.value,
            last_name: lastnameRef.current.value,
            detected_image: hexStr
        })
    }).then(res => console.log(res))
    }}

    reader.readAsArrayBuffer(file);
    }
 
     return (
        <OffCanvas title="Create user" button_text="Create User">
            <Form noValidate validated={validated} onSubmit={handleSubmit}>
                <Form.Group>
                    <Form.Label> Username </Form.Label>
                    <Form.Control type="text" placeholder="username"
                    required
                    ref={usernameRef}/>
                </Form.Group>
                <Form.Group>
                    <Form.Label> password </Form.Label>
                    <Form.Control
                    required
                    type="text" placeholder="password"
                    ref={passwordRef}/>
                </Form.Group>
                <Form.Group>
                    <Form.Label> First name </Form.Label>
                    <Form.Control 
                    required
                    type="text" placeholder="Jonh"
                    ref={firstnameRef}/>
                </Form.Group>
                <Form.Group>
                    <Form.Label> Last name </Form.Label>
                    <Form.Control type="text" placeholder="Dou"
                    required
                    ref={lastnameRef}/>
                </Form.Group>
                <Form.Group>
                    <Form.Label> Face image </Form.Label>
                    <Form.Control type="file"
                    required
                    ref={imageRef}/>
                </Form.Group>
                <Button type="submit" variant="primary" className="bg-primary">Submit form</Button>
            </Form>
            <div ref={errorRef}></div>
        </OffCanvas>
    )
}
