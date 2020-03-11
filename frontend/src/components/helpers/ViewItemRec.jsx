import React, { Component } from "react";
import "./styles.css";

class ViewItemRec extends Component {
  constructor(props) {
    super(props);
    this.state = {};
  }

  render() {
    return (
      <div
        style={{
          textAlign: "center",
          margin: "auto",
          width: "50%",
          border: "1px solid black"
        }}
      >
        <h5 className="viewHeading">Donation ID: {this.props.id}</h5>
        <h5 className="viewHeading">Reciever ID: {this.props.reciever}</h5>
        <h5 className="viewHeading">Distributor ID: {this.props.dist}</h5>
        <h5>Date: {this.props.date} </h5>
        <h5>FOOD ITEMS</h5>
        <table>
          <tr>
            <th>Food Name</th>
            <th>Quantity</th>
          </tr>
          {this.props.foods.map(food => (
            <tr>
              <td>{food.name}</td>
              <td>{food.quantity}</td>
            </tr>
          ))}
        </table>
      </div>
    );
  }
}

export default ViewItemRec;
