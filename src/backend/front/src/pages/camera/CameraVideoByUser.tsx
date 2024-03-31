import React, { useEffect, useState } from "react";
import { request } from "../../utils/request";
import { OffCanvas } from "../../components/OffCanvas";


interface IBox {
  top_x: number;
  top_y: number;
  bot_x: number;
  bot_y: number;
  user_id: number | null;
}

interface IFrameData {
  frame: string; // Assuming hexbytes are represented as strings
  created_at: string; // Date in ISO format
  boxes: IBox[];
}


export const CameraVideoByUser = ({ onAddComponent }: { onAddComponent: (component: React.ReactNode) => void }) => {

    const [currentData, setCurrentData] = useState<IFrameData[]>();

    const fetchFrameData = async (userId: number): Promise<IFrameData[]> => {
        const url = `/user/${userId}/frames`;
        return request({ method: 'GET', url }).then(data => data as IFrameData[]);
    };

    useEffect(() => {
        fetchFrameData(1)
            .then(frameData => {
                console.log(frameData);
                setCurrentData(frameData)
                console.log('susus')
            })
        .catch(error => {
        console.error("Failed to fetch frame data:", error);
        });
    }, [])    

    return (
    <>
        <OffCanvas title="Add camera by user" button_text="Add camera by user">
            <div>123</div>
        </OffCanvas>
    </>
    )
}

