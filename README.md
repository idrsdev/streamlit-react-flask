# Streamlit Custom Components

An App where we load react components into streamlit. The data can be received and passed to these react components. We also integrated Flask API to make our requests allowing us to utilize machine learning models deloyed with Flask

#### Overview

A Streamlit Component is made out of a Python API and a frontend (built using any web tech you prefer).

A Component can be used in any Streamlit app, can pass data between Python and frontend code, and and can optionally be distributed on [PyPI](https://pypi.org/) for the rest of the world to use.

-   Create a component's API in a single line of Python:

```python
import streamlit.components.v1 as components

# Declare the component:
my_component = components.declare_component("my_component", path="frontend/build")

# Use it:
my_component(greeting="Hello", name="World")
```

-   Build the component's frontend out of HTML and JavaScript (or TypeScript, or ClojureScript, or whatever you fancy). React is supported, but not required:

```typescript
class MyComponent extends StreamlitComponentBase {
    public render(): ReactNode {
        // Access arguments from Python via `this.props.args`:
        const greeting = this.props.args['greeting']
        const name = this.props.args['name']
        return (
            <div>
                {greeting}, {name}!
            </div>
        )
    }
}
```

#### How it works

`Each Streamlit call on the Python side loads up a React component from the running Streamlit server, which is then rendered onto your web browser.`

Streamlit components follow the same model:

1. A Streamlit Python call is mapped into a set of HTML/CSS/JS code or frontend code. Python arguments passed through the Streamlit call are then sent through the body of a JavaScript event. In the case of the React template, those arguments then become props of the React component.

2. The frontend component gets rendered inside an IFrame on the browser.

3. If the user interacts with the widget, then the component handles a callback which may modify the internal state of the frontend component — this will then send the value back to the Streamlit Python script through the body of a JavaScript event. This also triggers a rerun of the Python script where the Python variable returned by the Streamlit call gets assigned the new value.

![Overview](images/overview.PNG)

#### Reusability

Plus, given Streamlit’s design, a component cannot call nor interact with other components using callbacks. In the same way that you can write a Streamlit script without callbacks between components, you can write a frontend component code without worrying about its behavior if other widgets on the same page call it.

`It means we can create multiple clones of one component e.g we have reused the same Slider component with different parameters But they are independent of each other`

#### Docker Setup

```
docker-compose build
docker-compose up
# The App is available at http://localhost:8501/
```

#### How to Information

```
streamlit_custom_slider/__init__.py
# This is where we have declard connection to react Components and create custom streamlit components e.g st_custom_slider()
# one thing to note here is that You cannot connect with multiple react components on same route e.g '/'

# This is the workaround, to load more than one components, create different route for each component on react side.

```

##### Python Side

```
streamlit_custom_slider/__init__.py

#Since we cannot connect/load multiple components from one url, e.g url="http://localhost:3001/"
#Breaking components into multiple routes, e.g /dropdown, /slider.

_dropdown_func = components.declare_component(
    "custom_select",
    url="http://localhost:3001/dropdown",
)

#To connect with <CustomSlider /> on react side, Along with passing data this is how we do it,
_component_func = components.declare_component(
    "custom_slider",
    url="http://localhost:3001/slider",
)

# Arguments sent, accessible from props.args and result received from React component,

def st_custom_slider(label: str, min_value: int, max_value: int, value: int = 0, key=None) -> int:
    component_value = _component_func(label=label, minValue=min_value, maxValue=max_value, initialValue=[value], key=key, *default=[value]*)
    return component_value[0]

# As custom components return value to python scrips, initiallt the value is zero(The default value we set above)
```

##### React Side

```
// A routing Snipppets from index.tsx (React)
<Router>
         <Route path="/slider">
           <StyletronProvider value={engine}>
              <ThemeProvider theme={LightTheme}>
                <CustomSlider />
              </ThemeProvider>
            </StyletronProvider>
         </Route>

          <Route path="/dropdown">
            <CustomSelect />
          </Route>

      {/* <Route path="/dropdown">
            <Component Here />
          </Route>  */}
</Router>

//Two Important things, If you don't set the height, the component will not be visisble, taken from < CustomSelect />

useEffect(() => {
    Streamlit.setFrameHeight()
  })

//On Items like dropdown, to change component height on streamlit side on state toggle
 const onDropdownToggle = () => {
    Streamlit.setFrameHeight()
  }

//These components return value to streamlit, where they are loaded but how?
const onChange = (option) => {
    Streamlit.setComponentValue(option[0].value) //This sets the value of a component
    //Streamlit.setComponentValue(valueHere)
  }
```

##### Streamlit

```
app.py
#Importing Our Custom Component
from streamlit_custom_slider import st_custom_slider #from streamlit_custom_slider/__init__.py(Package)
#using them
input_features["age"] = st_custom_slider('Age', 18, 95, 50, key="age")


```

#### Local Setup

```
# Requirments
Python 3.7.1rc2
node v16.14.0.
```

Install and run streamlit locally

```
$ python -m venv venv  # create venv
$ . venv/bin/activate   # activate venv
$ pip install -r requirements.txt # installing libraries
# App.py - Line:11, Replace url value from docker to local
# url = 'http://pythonapi:5000' with url = 'http://localhost:5000'
$ streamlit run app.py # Runs on port localhost:8501
```

Install & Run Python/Flask API:

```
# Flask API and its dependencies exists in pythonapi folder
$ cd pythonapi
$ python -m venv venv  # create venv
$ . venv/bin/activate   # activate venv
$ pip install -r requirements.txt
$ python app.y
```

Our React App

```
# The whole react app exists in frontend folder
cd streamlit_custom_slider/frontend
npm install
npm run start
```
