// eslint-disable-next-line no-unused-vars
import * as React from "react";
import Navbar from "../Navbar";
import { Container, CssBaseline, Grid, Paper, Typography } from "@mui/material";

export default function Homepage() {
  return (
    // <Container component="main"     >
    <>
        <CssBaseline />
        <Navbar />
        <Grid container spacing={5} sx={{ mt: 3 }}>
            <Grid item xs={12} sm={6}>
                <Paper sx={{ p: 2, display: 'flex', flexDirection: 'column', height: 240 }}>
                    <Typography variant="h6" gutterBottom>
                        Circle 1
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                        Circle 2
                    </Typography>
                    <Typography variant="h6" gutterBottom>
                        Circle 3
                    </Typography>
                </Paper>
            </Grid>
        </Grid>
        
    
    {/* </Container> */}
    </>
  )
}
