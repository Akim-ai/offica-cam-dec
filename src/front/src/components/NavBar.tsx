import React from "react";
import Nav from "react-bootstrap/Nav";


const NavBar = () => {


    return (
        <Nav fill variant="tabs" defaultActiveKey="/">
            <Nav.Item>
                <Nav.Link eventKey="list-0" href="/">Video</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link eventKey="list-1" href="/cameras">Cameras</Nav.Link>
            </Nav.Item>
            <Nav.Item>
                <Nav.Link eventKey="link-2" href="/users">Detected Users</Nav.Link>
            </Nav.Item>
        </Nav>
    
    )
}

export default NavBar
