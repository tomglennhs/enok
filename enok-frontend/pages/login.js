import Navbar from "../components/Navbar";
import {Button} from "@chakra-ui/react";
import Script from "next/script";

export default function Home() {
    return (
        <>
            {/*<Button>*/}
            {/*    <a href={"/api/auth/google"}> Log in with Google</a>*/}
            {/*</Button>*/}
            <Script src="https://accounts.google.com/gsi/client" async defer></Script>
            <div id="g_id_onload"
                 data-client_id="583695242034-fhr45p5p5bf996hm3ihmvfa5kg7g1e4t.apps.googleusercontent.com"
                 data-login_uri="/api/auth/google"
                 data-auto_prompt="false">
            </div>
            <div className="g_id_signin"
                 data-type="standard"
                 data-size="large"
                 data-theme="outline"
                 data-text="sign_in_with"
                 data-shape="rectangular"
                 data-logo_alignment="left">
            </div>
        </>
    )
}
