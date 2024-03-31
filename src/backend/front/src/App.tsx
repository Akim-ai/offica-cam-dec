
import 'bootstrap/dist/css/bootstrap.min.css';


import { LoginPage } from "./pages/loginPage.tsx";
import IndexPage from "./pages";
import CameraPage from "./pages/cameraPage.tsx";
import {
    RouterProvider,
    createBrowserRouter,
} from "react-router-dom";

function App() {

    const router = createBrowserRouter([
        {
            id: "root",
            path: "/",
            children: [
                {
                    index: true,
                    Component: IndexPage,
                },
                {
                    path: "login",
                    // action: loginAction,
                    // loader: loginLoader,
                    Component: LoginPage,
                },
                {
                    path: "camera",
                    Component: CameraPage,
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
