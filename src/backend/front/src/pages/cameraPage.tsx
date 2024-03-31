import React, { useState, useCallback } from "react";
import { AddCamera } from "./camera/AddCamera";
import { ShowCamerasData } from "./camera/Cameras";
import { CameraVideoByUser } from "./camera/CameraVideoByUser";
import { ShowCameraVideo } from "./camera/ShowCameraVideo";
import { ShowUsers } from "./camera/ShowUsers";

const CameraPage = () => {
  const [components, setComponents] = useState<React.ReactNode[]>([]);

  const addComponent = useCallback((component: React.ReactNode) => {
    setComponents((prev) => [...prev, component]);
    console.log(component)
  }, []);
//  <ShowCameraVideo startDateTime={new Date().toISOString()}/>
  return (
    <div>
      <AddCamera/>
      <ShowCamerasData handleAddCamera={addComponent} />
      <ShowUsers handleAddCamera={addComponent}/>     
      {components.map((Component, index) => <React.Fragment key={index}>{Component}</React.Fragment>)}
     
    </div>
  );
};

export default CameraPage;
