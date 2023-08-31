import {Box,CssBaseline} from "@mui/material";
import PrimaryAppBar from "./PrimaryAppBar";
import PrimaryDraw from "./PrimaryDraw";
import SecondaryDraw from "./SecondaryDraw";
import Main from "./main"

const Home = () => {
    return (
    <Box sx={{display: "flex"}}>
        <CssBaseline/>
        <PrimaryAppBar/>
        
        <PrimaryDraw/>
        <SecondaryDraw/>
        <Main/>

        </Box>
    );
};

export default Home;