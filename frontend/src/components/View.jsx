import React from "react";
import { Button } from "@material-ui/core";
import ViewItemDon from "./helpers/ViewItemDon";
import ViewItemRec from "./helpers/ViewItemRec";

class View extends React.Component {
  constructor(props) {
    super(props);
    this.state = {
      donor: "",
      distDon: "",
      distRec: "",
      reciever: "",
      donations: [],
      reciepts: []
    };
    this.handleChange = this.handleChange.bind(this);
    this.onSubmitDon = this.onSubmitDon.bind(this);
    this.onSubmitRec = this.onSubmitRec.bind(this);
  }

  handleChange(event) {
    const target = event.target;
    const value = target.type === "checkbox" ? target.checked : target.value;
    const name = target.name;
    this.setState({
      [name]: value
    });
  }

  onSubmitDon(e) {
    e.preventDefault();
    fetch("/getDon", {
      method: "POST",
      body: JSON.stringify({
        donor: this.state.donor,
        dist: this.state.distDon
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(res => {
        this.setState({ donations: res.donations });
      });
  }
  onSubmitRec(e) {
    e.preventDefault();
    fetch("/getReciept", {
      method: "POST",
      body: JSON.stringify({
        reciever: this.state.reciever,
        dist: this.state.distDon
      }),
      headers: {
        "Content-Type": "application/json"
      }
    })
      .then(res => res.json())
      .then(res => {
        this.setState({ reciepts: res.reciepts });
      });
  }

  render() {
    const { selectedOption } = this.state;

    return (
      <div style={{ textAlign: "center" }}>
        <h1>View Donation</h1>
        <p>Note: Leave a Field blank to show all results</p>
        Donor ID:{" "}
        <input
          style={{ marginRight: "2%" }}
          type="text"
          name="donor"
          value={this.state.donor}
          onChange={this.handleChange}
        />
        Distributor ID:{" "}
        <input
          type="text"
          name="dist"
          value={this.state.dist}
          onChange={this.handleChange}
        />
        <br />
        <br />
        <Button variant="contained" color="primary" onClick={this.onSubmitDon}>
          Show Donations
        </Button>
        <br />
        <br />
        {this.state.donations.map(don => (
          <ViewItemDon
            id={don.id}
            donor={don.donor}
            dist={don.dist}
            date={don.date}
            foods={don.foods}
          />
        ))}
        <h1>View Reciept</h1>
        <p>Note: Leave a Field blank to show all results</p>
        Reciever ID:{" "}
        <input
          style={{ marginRight: "2%" }}
          type="text"
          name="reciever"
          value={this.state.reciever}
          onChange={this.handleChange}
        />
        Distributor ID:{" "}
        <input
          type="text"
          name="distRec"
          value={this.state.distRec}
          onChange={this.handleChange}
        />
        <br />
        <br />
        <Button variant="contained" color="primary" onClick={this.onSubmitRec}>
          Show Reciepts
        </Button>
        <br />
        <br />
        {this.state.reciepts.map(rec => (
          <ViewItemRec
            id={rec.id}
            reciever={rec.reciever}
            dist={rec.dist}
            date={rec.date}
            foods={rec.foods}
          />
        ))}
      </div>
    );
  }
}

export default View;
