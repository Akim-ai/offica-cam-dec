
import React, { useState, useEffect, useCallback, useRef } from 'react';
import { request } from '../../utils/request';

interface IShowCameraVideo{
    startDateTime: string;
    urlPrefix: string;
}

interface IBox {
  top_x: number;
  top_y: number;
  bot_x: number;
  bot_y: number;
  user_id: number | null;
}

interface IFrame {
  frame: string; // This will store base64-encoded image data
  created_at: string;
  boxes: IBox[];
}

interface IResult{
    next: string;
    data: IFrame[];
}

const ShowCameraVideo = (props: IShowCameraVideo) => {
  const [frames, setFrames] = useState<IResult>(); // Adjust based on your data structure
  const [error, setError] = useState<string | null>(null);
  const [currentIndex, setCurrentIndex] = useState<number>(-1);
  const canvasRef = useRef<HTMLCanvasElement>(null);
  const [nextFrames, setNextFrames] = useState<IResult>();
  const [isRequestInProgress, setIsRequestInProgress] = useState<boolean>(false);

  useEffect(() => {fetchFrames(props.startDateTime, false)}, [])
  


  const fetchFrames = useCallback(async (start: string, next: boolean) => {
      console.log(props.startDateTime, start);
    if (isRequestInProgress) {
        console.log("req in prog")
      return; // Early return if a request is already in progress
    }
    setIsRequestInProgress(() => true); // Set request status to in progress
    request({ method: 'GET', url: `${props.urlPrefix}?start=${start.replace("+00:00", "")}` })
      .then(async data => {
          if (data?.data && data.data.length <= 2){
            async function sleep(ms: number){
                new Promise(resolve => setTimeout(resolve, ms));
                setNextFrames((prev) => {
                    if (!prev?.next){
                        return prev;
                    }
                    let next = new Date(prev?.next).getTime()+ms;
                    const max_time = new Date().getTime()-10*1000;
                    if (next > max_time)
                        next = max_time;
                    prev.next = new Date(next).toISOString();
                    return prev;

                })
                setIsRequestInProgress(false)
                }
            await sleep(1000)
            return

        }
        console.log(data)
        if (!data?.data?.length){return }
        const processedData: IResult = {
            next: data.next,
            data: data.data.map((frame: any) => ({
                ...frame,
                created_at: new Date(frame.created_at).toISOString(), // Convert to UTC
            })),
            }
        if (!next){
            setFrames(processedData);
            setNextFrames(processedData)
            setCurrentIndex(0);
            console.log(`req if ${0}`)
        } else {
            setNextFrames(() => processedData);
        }
        setIsRequestInProgress(false); // Reset request status after completion
      })
      .catch(err => {
        console.error(err);
        setError('Failed to fetch frames');
        
        setIsRequestInProgress(false); // Reset request status on error
      });
  }, [isRequestInProgress]);

  useEffect(() => {
    const canvas = canvasRef.current;
    const context = canvas?.getContext('2d');
    if (frames?.data && frames.data.length > 0 && frames?.data.length > currentIndex+1) {
      const currentTime = new Date(frames?.data[currentIndex].created_at).getTime();
      const nextTime = new Date(frames?.data[currentIndex + 1].created_at).getTime();
      const diffTime = nextTime - currentTime;
      console.log(diffTime)
      if (diffTime < 0){
        if (!nextFrames?.next){ return }
        fetchFrames(nextFrames.next, true)
        return
      }
      const timer = setTimeout(() => {
        setCurrentIndex(currentIndex + 1);
      }, diffTime);
      if (context) {
        if (currentIndex === Math.floor(frames.data.length/2)-1){
            console.log(currentIndex, nextFrames?.next);
            if (nextFrames?.next) {
                fetchFrames(nextFrames.next, true)
            }
        }
      const currentFrame = frames.data[currentIndex];
      const image = new Image();
      image.onload = () => {
        if (canvas) {
          canvas.width = image.width;
          canvas.height = image.height;
          context.clearRect(0, 0, canvas.width, canvas.height);
          context.drawImage(image, 0, 0);
          currentFrame.boxes.forEach(box => {
            context.beginPath();
            context.rect(box.top_x, box.top_y, box.bot_x - box.top_x, box.bot_y - box.top_y);
            context.strokeStyle = 'red';
            context.stroke();
            if (box.user_id !== null) {
                const text = `User ID: ${box.user_id}`;
                const textX = box.top_x; // You might want to adjust this position
                const textY = box.bot_y + 15; // Adjust as needed to position below the box
                context.fillStyle = 'black'; // Text color
                context.fillText(text, textX, textY);
            }
          });
        }
      };
      image.src = `http://127.0.0.1:8000/${currentFrame.frame}`;
    }
    console.log(`timer clearned ${currentIndex}:${frames.data[currentIndex].created_at}`)
      return () => clearTimeout(timer);

    } else if (!frames?.data){
        console.log("nodata", frames)

    }else if (currentIndex >= frames?.data?.length - 1) {
        setFrames(() => nextFrames);
        setCurrentIndex(() => 0);
    } else {
        console.log(`No conditions ${nextFrames?.data.length}:${frames?.data.length}:${currentIndex}`);
    }
    }, [frames, currentIndex]);

  return (

      <canvas ref={canvasRef}></canvas>
    )
};

export { ShowCameraVideo };
