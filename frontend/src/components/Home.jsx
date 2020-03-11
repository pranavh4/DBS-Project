import React, { Component } from "react";
import { Link } from "react-router-dom";

class Home extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }
  render() {
    return (
      <div style={{ margin: "auto", width: "50%", textAlign: "center" }}>
        <h2 style={{ padding: "5% 0" }}>
          View Donations <Link to="/View">Click Here</Link>
        </h2>
        <h2 style={{ padding: "5% 0" }}>
          Add Donations <Link to="/Add">Click Here</Link>
        </h2>
        <h2 style={{ padding: "5% 0" }}>
          Register as Donating Organization{" "}
          <Link to="/DonorReg">Click Here</Link>
        </h2>
        <h2 style={{ padding: "5% 0" }}>
          Register as Recieving Organization{" "}
          <Link to="/RecieverReg">Click Here</Link>
        </h2>
        <h2 style={{ padding: "5% 0" }}>
          Register as Distributor <Link to="/DistributorReg">Click Here</Link>
        </h2>
        <h2 style={{ padding: "5% 0" }}>
          Add Food Item <Link to="/Food">Click Here</Link>
        </h2>
      </div>
    );
  }
}

export default Home;
