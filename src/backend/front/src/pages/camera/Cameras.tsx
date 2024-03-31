import React, { MouseEventHandler, useEffect, useState } from "react";
import { OffCanvas } from "../../components/OffCanvas"; 
import { Button, Pagination, Table } from "react-bootstrap";
import { request } from "../../utils/request";
import { ShowCameraVideo } from "./ShowCameraVideo";

interface ICamera{
    id: number;
    name: string;
    ip_endpoint: string;
    is_active: boolean;
}


interface IShowCamerasData {
    handleAddCamera: Function;
}


export const ShowCamerasData = (props: IShowCamerasData) => {
    
    const [page, setPage] = useState<number>(1);
    const [cameras, setCameras] = useState<ICamera[]>([]);
    const [loading, setLoading] = useState<boolean>(true);

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
    }

    useEffect(() => {
        get_cameras();
    }, [page]);

    const addCameraButton = (id_: number) => {
        return <Button variant="primary" onClick={() => props.handleAddCamera(<ShowCameraVideo urlPrefix={`camera/${id_}/frame`} startDateTime={new Date().toISOString()}/>)}>add camera</Button>
    }

    return (
        <OffCanvas onClick={get_cameras} title="Cameras" button_text="Cameras List">
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
                            <tr key={camera.id}>
                                <td>{addCameraButton(camera.id)}</td>
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
            <Pagination>
                
            </Pagination>
        </OffCanvas>
    )
}

