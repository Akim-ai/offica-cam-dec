import React, { useState } from "react";
import { Button, Offcanvas, Table } from "react-bootstrap";
import { ShowCameraVideo } from "./ShowCameraVideo";
import { OffCanvas } from "../../components/OffCanvas";
import { request } from "../../utils/request";

interface IShowUsers {
    handleAddCamera: Function;
}

interface IUser{
    first_name: string;
    last_name: string;
    id: number;
    detected_path_image: string;
}

interface IUsersPagination{
    data: IUser[];
    next: boolean;
    count: number;
}

export const ShowUsers = (props: IShowUsers) => {

    const [loading, setLoading] = useState<boolean>(true);
    const [users, setUsers] = useState<IUsersPagination>();
    const [page, setPage] = useState<number>(1)

    const handleGetUsers = () => {
        setLoading(true)
        request({"url": `user/?page=${page}`,"method": "GET"})
        .then(data => {
            setUsers(data);
            setLoading(false)
        })
    }
    
    const handleAddCameraUser = (userId: number) => {
        return <Button  className="me-2 bg-primary" variant="primary" onClick={() => props.handleAddCamera(<ShowCameraVideo urlPrefix={`user/${userId}/frame`} startDateTime={new Date().toISOString()}/>)}>add camera</Button>
    }

    return (
        <OffCanvas onClick={handleGetUsers} title="Users" button_text="Users List">
            <Button  className="me-2 bg-primary" variant="primary">Add user</Button>
            <Button  className="me-2 bg-primary" variant="primary">Add Anonymous</Button>
            <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <th>Add video by user</th>
                        <th>ID</th>
                        <th>First Name</th>
                        <th>Last name</th>
                    </tr>
                </thead>
                <tbody>
                    {loading ? (
                        <tr><td colSpan={4}>Loading...</td></tr>
                    ) : (users?.data?.length && users.data.length > 0) ? (
                        users.data.map((user) => (
                            <tr key={user.id}>
                                <td>{handleAddCameraUser(user.id)}</td>
                                <td>{user?.id}</td>
                                <td>{user?.first_name}</td>
                                <td>{user?.last_name}</td>
                                <td> <Button  className="me-2 bg-red-700" variant="danger">Delete user</Button></td>
                            </tr>
                        ))
                    ) : (
                        <tr><td colSpan={4}>No cameras found.</td></tr>
                    )}
                </tbody>
            </Table>
        </OffCanvas>
    )
}
