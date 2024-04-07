
import 'bootstrap/dist/css/bootstrap.min.css';


import CameraPage from "./pages/cameraPage.tsx";
import {
    RouterProvider,
    createBrowserRouter,
} from "react-router-dom";
import CamerasPage from './pages/CamerasPage.tsx';
import UsersPage from './pages/UsersPage.tsx';

function App() {

    const router = createBrowserRouter([
        {
            id: "root",
            path: "/",
            children: [
                {
                    index: true,
                    Component: CameraPage,
                },
                //{
                  //  path: "login",
                    // action: loginAction,
                    // loader: loginLoader,
                    //Component: LoginPage,
                //},
                {
                    path: "cameras",
                    Component: CamerasPage,
                },
                {
                    path: "users",
                    Component: UsersPage,
                },
            ],
        }
        ]
    )

  return (
      <RouterProvider router={router} fallbackElement={<p>Initial Load...</p>} />
  )
}

export default App
