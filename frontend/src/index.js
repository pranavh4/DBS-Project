import React from "react";
import ReactDOM from "react-dom";
import "./index.css";
// import App from "./App";
import * as serviceWorker from "./serviceWorker";
import "bootstrap/dist/css/bootstrap.css";
import { BrowserRouter as Router, Route, Switch } from "react-router-dom";
import Home from "./components/Home";
import OrgReg from "./components/OrgReg";
import Add from "./components/Add";
import View from "./components/View";
import Food from "./components/Food";

const App = () => (
  <Router>
    <Switch>
      <Route exact path="/" component={Home} />
      <Route exact path="/DonorReg" render={() => <OrgReg type={"Donor"} />} />
      <Route
        exact
        path="/RecieverReg"
        render={() => <OrgReg type={"Reciever"} />}
      />
      <Route
        exact
        path="/DistributorReg"
        render={() => <OrgReg type={"Distributor"} />}
      />
      <Route exact path="/Add" component={Add} />
      <Route exact path="/View" component={View} />
      <Route exact path="/Food" component={Food} />
    </Switch>
  </Router>
);

ReactDOM.render(<App />, document.getElementById("root"));

// If you want your app to work offline and load faster, you can change
// unregister() to register() below. Note this comes with some pitfalls.
// Learn more about service workers: https://bit.ly/CRA-PWA
serviceWorker.unregister();
