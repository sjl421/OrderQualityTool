var models = require("./models");
var BaseTest = Object.create(null);
var group1Cycles = [
    {id: "Current", name: "Current Cycle"}
];
var group2Cycles = [
    {id: "Current", name: "Current Cycle"},
    {id: "Previous", name: "Previous Cycle"}
];
FacilityTest = function (metaData) {
    return {
        newGroup:
            function (groupNumber) {
                return {
                    cycles: groupNumber === 1 ? group1Cycles : group2Cycles,
                    cycle: group1Cycles[0],
                    model: this.models[0],
                    aggregation: this.calculations[0],
                    selected_fields: [],
                    selected_formulations: [],
                    sample_formulation_model_overridden: {},
                    sample_formulation_model_overrides: {},
                    name: "G" + groupNumber
                };

            },
        getGroups: function (metaData) {
            return [
                this.newGroup(1, metaData),
                this.newGroup(2, metaData)
            ];
        },
        id: "FacilityTwoGroups",
        name: "Facility with 2 Groups of data",
        comparisons: [
            {id: "LessThan", name: "Percentage Variance is less than N%"},
            {id: "NNRTILessThan", name: "FOR NNRTI Percentage Variance is less than N%"},
            {id: "AtLeastNOfTotal", name: "Group1 Is at least N% of the total"},
            {id: "AreEqual", name: "Are Equal"},
            {id: "AreNotEqual", name: "Are Not Equal"},
            {id: "NoNegatives", name: "Has No Negatives"},
            {id: "NoBlanks", name: "Has No Blanks"}
        ],
        calculations:
            [
                {id: "SUM", name: "Sum"},
                {id: "AVG", name: "Average"},
                {id: "VALUE", name: "Values"}
            ],
        models:
            [
                models.newModel("Adult", "Adult Records", metaData, "FacilityTwoGroups"),
                models.newModel("Paed", "Paed Records", metaData, "FacilityTwoGroups"),
                models.newModel("Consumption", "Consumption Records", metaData, "FacilityTwoGroups")
            ]
    };
};

var FacilityTestWithTracingFormulation = function (metaData) {
    var test = FacilityTest(metaData);
    test.id = "FacilityTwoGroupsAndTracingFormulation";
    test.name = "Facility with 2 Groups And Tracing Formulation";
    test.models = [
        models.newTracingModel("Adult", "Adult Records", metaData, "FacilityTwoGroupsAndTracingFormulation", true),
        models.newTracingModel("Paed", "Paed Records", metaData, "FacilityTwoGroupsAndTracingFormulation", true),
        models.newTracingModel("Consumption", "Consumption Records", metaData, "FacilityTwoGroupsAndTracingFormulation")
    ];
    return test;
};

var SingleGroupFacilityTest = function (metaData) {
    var test = FacilityTest(metaData);
    test.id = "FacilityOneGroup";
    test.name = "Facility with 1 Group";
    test.getGroups = function (metaData) {
        return [
            test.newGroup(1, metaData)
        ];
    };

    test.calculations = [
        {id: "VALUE", name: "Values"}
    ];

    test.comparisons = [
        {id: "NoNegatives", name: "Has No Negatives"},
        {id: "NoBlanks", name: "Has No Blanks"}
    ];
    return test;
};

var getTypeFromJSON = function (metaData, typeData) {
    if (typeData.id === "FacilityTwoGroups") {
        return FacilityTest(metaData);
    }
    if (typeData.id === "FacilityTwoGroupsAndTracingFormulation") {
        return FacilityTestWithTracingFormulation(metaData);
    }

    if (typeData.id === "FacilityOneGroup") {
        return SingleGroupFacilityTest(metaData);
    }

    if (typeData.id === "ClassBased") {
        return ClassBasedTest(metaData);
    }
};

function rebuildGroupsFromJSON(groups, testType, metaData) {
    var count = 0;
    return _.map(groups, function (group) {
        if (testType.id === "FacilityTwoGroups" || testType.id === "FacilityOneGroup") {
            group.model = models.newModel(group.model.id, group.model.name, metaData, testType.id);
        }
        if (testType.id === "FacilityTwoGroupsAndTracingFormulation") {
            group.model = models.newTracingModel(group.model.id, group.model.name, metaData, testType.id, group.model.allowOverride);
        }
        group.cycles = count === 0 ? group1Cycles : group2Cycles;
        count += 1;
        return group;
    });
}

var buildDefinition = function (inputValue, metaData) {
    var definition = JSON.parse(inputValue);
    definition.type = getTypeFromJSON(metaData, definition.type);
    if (definition.groups) {
        definition.groups = rebuildGroupsFromJSON(definition.groups, definition.type, metaData);
    }
    return definition;
};
var ClassBasedTest = function (metaData) {
    var test = {};
    test.id = "ClassBased";
    test.name = "Class Based Facility Check";
    test.getGroups = function (metaData) {
        return [];
    };

    test.calculations = [];

    test.comparisons = [];
    return test;
};
module.exports = {
    FacilityTest: FacilityTest,
    FacilityTestWithTracingFormulation: FacilityTestWithTracingFormulation,
    SingleGroupFacilityTest: SingleGroupFacilityTest,
    ClassBasedTest: ClassBasedTest,
    buildDefinition: buildDefinition
};