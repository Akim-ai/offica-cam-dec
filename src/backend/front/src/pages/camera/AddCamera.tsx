import React, { MouseEventHandler, MutableRefObject, useRef } from "react";
import { OffCanvas } from "../../components/OffCanvas";
import { Button, Form } from "react-bootstrap";
import { request } from "../../utils/request";

export const AddCamera = () => {

    const ipRef = useRef<MutableRefObject<HTMLInputElement>>();
    const nameRef = useRef();

    const handleSubmit = () => {
        if (!ipRef?.current){
            return
        }
        if (!nameRef?.current){
            return
        }
        const ip = ipRef.current?.value;
        const name = nameRef.current?.value;

        request({url: "camera/", method: "POST",
            body: JSON.stringify({ip_endpoint: ip, name: name})
        })
        .then(res => console.log(res))
    }

    return (
        <OffCanvas title="add camera" button_text="AddCamera">
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Camera IP</Form.Label>
                    <Form.Control type="text" placeholder="127.0.0.1:123/"
                    ref={ipRef}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Camera Name</Form.Label>
                    <Form.Control type="text" rows={3} placeholder="Unique name for camera"
                    ref={nameRef}
                    />
                </Form.Group>
                <Button variant="primary" className="bg-primary" onClick={handleSubmit}>
                    Submit Camera
                </Button>
                
            </Form>
        </OffCanvas>
    )
}

