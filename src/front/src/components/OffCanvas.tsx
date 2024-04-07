import React, { useState } from 'react';
import Button from 'react-bootstrap/Button';
import Offcanvas from 'react-bootstrap/Offcanvas';

interface IOffCanvas{
    title: string;
    button_text: string;
    children: JSX.Element[] | JSX.Element;
    onClick?: Function;
    placement?: string;
}


function OffCanvas(props: IOffCanvas) {
  const [show, setShow] = useState(false);
    
  const placement = props?.placement ? props.placement : 'start'

  const handleClose = () => {
    setShow(false);
    }
  const handleShow = () => {
      setShow(true);
    
    if (props?.onClick){
        props.onClick()
        }
    }
  return (
  <>
      <Button variant="primary" onClick={handleShow} className="me-2 bg-primary">
        {props.button_text}
      </Button>
      <Offcanvas show={show} className="w-1/3" onHide={handleClose} placement={placement}>
        <Offcanvas.Header closeButton>
          <Offcanvas.Title>{props.title}</Offcanvas.Title>
        </Offcanvas.Header>
        <Offcanvas.Body>
            {props.children}
        </Offcanvas.Body>
      </Offcanvas>
    </>
  );
}

export {OffCanvas}
