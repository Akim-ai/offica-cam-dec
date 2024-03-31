import React, { MutableRefObject, useRef, useState } from "react";
import { ICamera } from "./Cameras";
import { Button, Form, Offcanvas } from "react-bootstrap";
import { request } from "../../utils/request";

interface IUpdateCamera{
    setShowState: Function;
    showState: boolean;
    camera: ICamera;
}

export const UpdateCamera = (props: IUpdateCamera) => {

    const ipRef = useRef<MutableRefObject<HTMLInputElement>>();
    const nameRef = useRef<MutableRefObject<HTMLInputElement>>();
    const isActiveRef = useRef<MutableRefObject<HTMLInputElement>>();


    const getRefValue = (ref: MutableRefObject<any>) => {
        if (!ref?.current){
            return {"error": "no current Reference"}
        }
        if (!ref?.current?.value){
            return {"error": "No value"}
        }
        return ref.current.value
    }

    const handleSubmit = () => {

    
        request({ url: "camera/", method: "PUT",
        body: JSON.stringify({
                ip_endpoint: getRefValue(ipRef),
                name: getRefValue(nameRef),
                is_active: getRefValue(isActiveRef)
            })
        })
        .then(res => console.log(res));
    }

    return (
        <Offcanvas show={props.showState} placement="bottom" onHide={props.setShowState}>
            <Offcanvas.Header closeButton>
              <Offcanvas.Title>Update Camera</Offcanvas.Title>
            </Offcanvas.Header>
            
            <Offcanvas.Body>
            <Form>
                <Form.Group className="mb-3">
                    <Form.Label>Camera IP</Form.Label>
                    <Form.Control type="text" defaultValue={props.camera.ip_endpoint} placeholder="127.0.0.1:123/"
                    ref={ipRef}/>
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label>Camera Name</Form.Label>
                    <Form.Control type="text" rows={3} defaultValue={props.camera.name} placeholder="Unique name for camera"
                    ref={nameRef}
                    />
                </Form.Group>
                <Form.Group className="mb-3">
                    <Form.Label> Is active </Form.Label>
                    <Form.Check type="checkbox" defaultValue={props.camera.is_active} ref={isActiveRef}></Form.Check>
                </Form.Group>
                <Button variant="primary" className="bg-primary" onClick={handleSubmit}>
                    Submit Camera
                </Button>
            </Form>
            </Offcanvas.Body>
        </Offcanvas>
    )
}
