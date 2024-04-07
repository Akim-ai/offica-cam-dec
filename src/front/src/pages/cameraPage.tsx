import { useState, useEffect } from "react";
import { ShowCameraVideo } from "./camera/ShowCameraVideo";
import NavBar from "../components/NavBar";

export interface IComponent{
    ip_endpoint: string;
}

const CameraPage = () => {
  const [components, setComponents] = useState<string | null>(null);

  const componentKey: string = "cameras"

  const getComponentStr = () => {
    return localStorage.getItem(componentKey)
  }

  const checkComponent = () => {
      const componentsStr = getComponentStr()
      if (components === componentsStr){
        return
      }
      setComponents(componentsStr)
  };

  useEffect(() => {
    checkComponent()
    const interval = setInterval(checkComponent, 10000)

    return () => {
        clearInterval(interval)
    }
  }, [])

  const showComponents = () => {
    
    if (!components){return <div></div>}

    const cameras = JSON.parse(components)
    console.log(cameras)
    if(cameras.length === 0){return <div></div>}
    console.log(        cameras.map((camera_url) => {
         return <ShowCameraVideo
         urlPrefix={camera_url}
         startDateTime={new Date().toISOString()}
         />
        })

    )

    return (
        cameras.map((camera_url) => {
         return <ShowCameraVideo
         urlPrefix={camera_url}
         startDateTime={new Date().toISOString()}
         />
        })

    )
  }

  return (
    <>
        <NavBar/>

        <div>
            
            {showComponents()} 
        </div>
    </>
  );
};

export default CameraPage;
