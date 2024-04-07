import React, { MouseEventHandler, useEffect, useState } from "react";
import { Button, Container, Table } from "react-bootstrap";
import { request } from "../../utils/request";
import { ShowCameraVideo } from "./ShowCameraVideo";
import { AddCamera } from "./AddCamera";

export interface ICamera{
    id: number;
    name: string;
    ip_endpoint: string;
    is_active: boolean;
}


export const ShowCamerasData = () => {
    
    const [page, setPage] = useState<number>(1);
    const [cameras, setCameras] = useState<ICamera[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

    const [update, setUpdate] = useState<boolean>(false);
    const [camera, setCamera] = useState<ICamera>();

    const get_cameras = () => {
        setLoading(true);
        request({"url": `camera/list/?page=${page}`, "method":"GET"})
            .then(data => {
                console.log(data)
                setCameras(data.data);
                setLoading(false);
            })
            .catch(error => {
                console.error('Error fetching cameras:', error);
                setLoading(false);
            });
    }

    const handlePagination = (e: MouseEventHandler) => {
        setPage((prev) => prev+1)
    }

    const handleCreateCamera = (id: number) => {
    }

    useEffect(() => {
        get_cameras();
    }, [page]);

    const addCameraButton = (ip_endpoint: string) => {
        let addedCameras = localStorage.getItem("cameras");
        if (addedCameras == null){
            localStorage.setItem("cameras", JSON.stringify([ip_endpoint]))
            return
        }
        console.log(addedCameras)
        addedCameras = JSON.parse(addedCameras);
        localStorage.setItem("cameras", JSON.stringify([...addedCameras, ip_endpoint].filter((value, index, array) => array.indexOf(value) === index)))
    }

    const handleCameraEdit = (e: React.MouseEvent<HTMLTableRowElement, MouseEvent>, _camera: ICamera) => {
      if ((e.target as HTMLElement).tagName === 'BUTTON') {
        return
      }

      setCamera(_camera);
 
      setUpdate(true);
    }

    return (
    <Container>
        <AddCamera/>
        <Table striped bordered hover responsive>
                <thead>
                    <tr>
                        <th>AddCamera</th>
                        <th>ID</th>
                        <th>Name</th>
                        <th>IP Endpoint</th>
                        <th>Status</th>
                    </tr>
                </thead>
                <tbody>
                    {loading ? (
                        <tr><td colSpan={4}>Loading...</td></tr>
                    ) : (cameras?.length && cameras.length > 0) ? (
                        cameras.map((camera) => (
                            <tr key={camera.id} onClick={(e) => handleCameraEdit(e, camera)}>
                                <td><Button variant="primary" className="bg-primary" onClick={() => addCameraButton(`camera/${camera.id}/frame`)}>Add Camera</Button></td>
                                <td>{camera?.id}</td>
                                <td>{camera?.name}</td>
                                <td>{camera?.ip_endpoint}</td>
                                <td>{camera?.is_active ? "Active" : "Inactive"}</td>
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

