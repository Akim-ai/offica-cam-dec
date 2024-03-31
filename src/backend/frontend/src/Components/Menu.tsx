import React from "react";
import {NavigationMenuItem, NavigationMenuLink, navigationMenuTriggerStyle} from "@/components/ui/navigation-menu"
import {Link} from "lucide-react";

interface IMenu{
}

const Menu = (props: IMenu) => {


    return (
        <NavigationMenuItem>
            <Link href="/docs">
                <NavigationMenuLink className={navigationMenuTriggerStyle()}>
                    Documentation
                </NavigationMenuLink>
            </Link>
        </NavigationMenuItem>
    )
}
export default Menu