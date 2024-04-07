import React, { useEffect, useState } from "react";
import { Button, Container, Offcanvas, Table } from "react-bootstrap";
import { ShowCameraVideo } from "./ShowCameraVideo";
import { OffCanvas } from "../../components/OffCanvas";
import { request } from "../../utils/request";
import { AddUser } from "./AddUser";


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

export const ShowUsers = () => {

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

    useEffect(() => {
        handleGetUsers()
    }, [])

    const handleAddCameraByUser = (ip_endpoint: string) => {
        let addedCameras = localStorage.getItem("cameras");
        if (addedCameras == null){
            localStorage.setItem("cameras", JSON.stringify([ip_endpoint]))
            return
        }
        console.log(addedCameras)
        addedCameras = JSON.parse(addedCameras);
        localStorage.setItem("cameras", JSON.stringify([...addedCameras, ip_endpoint].filter((value, index, array) => array.indexOf(value) === index)))
    }

    const handleDeleteUser = (userId: number) => {
      request({"url": `user/${userId}`, "method": "DELETE"})
      .then(data => {
        console.log(data);
        handleGetUsers()
      })
    }

    return (
        <Container className="mt-2">
            <Container className="">

                <AddUser/>
                <Button  className="me-2 bg-primary" variant="primary">Add Anonymous</Button>
            </Container>
            <Table striped bordered hover responsive className="mt-8">
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
                                <td><Button  className="me-2 bg-primary" variant="primary" onClick={() => {handleAddCameraByUser(`user/${user.id}/frame`)}}>Add camera by user</Button></td>
                                <td>{user?.id}</td>
                                <td>{user?.first_name}</td>
                                <td>{user?.last_name}</td>
                                <td> <Button  className="me-2 bg-red-700" variant="danger"
                                onClick={() => handleDeleteUser(user.id)}
                                >Delete user</Button></td>
                            </tr>
                        ))
                    ) : (
                        <tr><td colSpan={4}>No cameras found.</td></tr>
                    )}
                </tbody>
            </Table>
        </Container>
    )
}
