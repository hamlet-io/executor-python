import os
from jinja2 import Template


class Group(object):
    """
    A cluster of entities
    """

    def __init__(self, dit):
        self.parentID = dit["parentID"]
        self.groupID = dit["groupID"]
        self.childIDs = []
        self.entities = []
        self.template = ""
        self.entityStr = ""
        self.rank = 0  # the rank of groups increment as it goes deeper
        self.libraries = []

    def findChildGroups(self, groups):
        """
        find child groups for parent groups, store childIDs for group object
        """
        for group in groups:
            if group.parentID == self.groupID and group != self:
                self.childIDs.append(group)

    def findEntities(self, entitiesGroup):
        """
        find entities of each group, store entities for group object
        """
        for en in entitiesGroup:
            if en["groupID"] == self.groupID:
                self.libraries.append(en["type"])  # save for library import
                en["type"] = en["type"].split(".")[-1]  # retrieve the last word as type
                self.entities.append(en)

    def createCluster(self):
        """
        create Cluster template
        """
        template = Template(
            """\
                with Cluster("{{groupID}}"):
                    {% for entity in entities %}
                    {{entity.entityID}}={{entity.type}}("{{entity.entityName}}")
                    {% endfor %}
            """
        ).render(groupID=self.groupID, entities=self.entities)
        self.entityStr = template
        self.template = template
        return self.template


def create_script(diagram, image_filename, temp_path):
    """
    Generates a diagrams formatted python script
    """

    diagramName = diagram["diagramName"]
    groups = diagram["groups"]
    entities = diagram["entities"]
    relationships = diagram["relationships"]

    image_filename = os.path.splitext(image_filename)[0]

    # build all group objects and store in list
    # create list of group objects, array in json is list in python
    groupObjects = []  # it has the length of group list
    for group in groups:
        groupObjects.append(Group(group))

    # find entities for each group and store
    for groupObj in groupObjects:
        groupObj.findEntities(entities)

    # match rank for each group and store
    rank_list = []

    def matchRank(groupObjects):
        allobjects = groupObjects.copy()
        if rank_list == []:
            for obj in groupObjects:
                # identify and remove groups with no parent
                if obj.parentID == "":
                    obj.rank = 1
                    rank_list.append(obj)
                    allobjects.remove(obj)
            groupObjects = allobjects
            matchRank(groupObjects)
        else:
            if allobjects != []:  # there are still objs unmatched
                for pa_obj in rank_list:
                    for obj in groupObjects:
                        if pa_obj.groupID == obj.parentID:
                            obj.rank = pa_obj.rank + 1
                            rank_list.append(obj)
                            allobjects.remove(obj)
                groupObjects = allobjects
                matchRank(groupObjects)
            else:
                return rank_list

    matchRank(groupObjects)

    # find child groups for each group and create template
    childGroups = []
    for groupObj in groupObjects:
        groupObj.findChildGroups(groupObjects)  # childIDs list is populated
        groupObj.createCluster()
        if (
            groupObj.childIDs == []
        ):  # if this group object has no child groups, save it as its own child group???
            childGroups.append(groupObj)

    def removeDuplicates(list):
        new_list = []
        for li in list:
            if li not in new_list:
                new_list.append(li)
        return new_list

    def findParents(childGroups, allObjects, rootGroups):
        """
        find parent group for each child group and combine Clusters
        """
        parentIDs = []
        for child in childGroups:
            if child.parentID == "":
                rootGroups.append(child)
            else:
                parentIDs.append(child.parentID)
        if parentIDs == []:
            return "all groups are root groups", removeDuplicates(rootGroups)
        parentIDs = removeDuplicates(parentIDs)

        parentsList = []
        for parent in parentIDs:
            template = Template(
                """\n
            with Cluster("{{parentID}}"):
                {% for child in childGroups %}
                {% if child.parentID == parentID %}
                {{child.template}}
                {% endif %}
                {% endfor %}
            """
            ).render(parentID=parent, childGroups=childGroups)
            for obj in allObjects:
                if obj.groupID == parent:
                    obj.template = obj.template + template
                    parentsList.append(obj)

        return findParents(parentsList, allObjects, rootGroups), removeDuplicates(
            rootGroups
        )

    # write all parent groups into template file
    with open(temp_path, "w+", encoding="utf-8") as f:
        for g in findParents(childGroups, groupObjects, [])[1]:
            f.write(g.template)

    # retrive parent groups file and remove redundant spaces. (Jinja2 template generates lots of spaces and empty lines)
    with open(temp_path, "r", encoding="utf-8") as f:
        lines = []
        for line in f.readlines():
            if line.strip() != "":
                lines.append(line)

    # insert remaining entities if there are any
    for obj in groupObjects:
        if obj.entities != [] and obj.childIDs != []:
            str = 'with Cluster("{}"):'.format(obj.groupID)
            lines = [obj.entityStr if l == str else l for l in lines]

    # write template in file
    with open(temp_path, "w+", encoding="utf-8") as f:
        for l in lines:
            f.write(l + "\n")

    # remove redundant spaces and empty lines
    with open(temp_path, "r", encoding="utf-8") as f:
        lines = f.readlines()
        lines = [l.strip() for l in lines]
        lines = [l for l in lines if l != ""]
        lines = removeDuplicates(lines)

        # get group rank for Cluster
        def clusterRank(str):
            name = str.split('"')[1].split('"')[0]
            for obj in groupObjects:
                if obj.groupID == name:
                    return obj.rank

        # import libraries from entity types
        import_diagrams = (
            "import diagrams\n"
            "from diagrams import Cluster, Diagram, Edge\n"
            "from diagrams.generic.blank import Blank\n"
        )
        imported_libraries = []
        for obj in groupObjects:
            for diagClass in obj.libraries:
                library = diagClass.rsplit(".", 1)[0]
                if library not in imported_libraries:
                    imported_libraries.append(library)
                    import_libray = "from {} import *\n".format(library)
                    import_diagrams = import_diagrams + import_libray

        exe_temp = (
            import_diagrams
            + f'\nwith Diagram("{diagramName}", show=False, outformat="png",'
            + f'filename="{image_filename}", direction="TB"):\n'
        )
        space = "    "  # indent
        rank = 0
        for i in range(len(lines)):
            if "with" in lines[i]:
                rank = clusterRank(lines[i])
                lines[i] = space * rank + lines[i] + "\n"  # indent according to ranks
            else:
                if "with" in lines[i - 1]:
                    rank = rank + 1
                lines[i] = space * rank + lines[i] + "\n"
            exe_temp = exe_temp + lines[i]

    # add relationships
    for rela in relationships:
        if isinstance(rela, dict):
            if rela["direction"] == "one way":
                rela_str = f'{space}{rela["startEntityID"]} >> Edge() >> {rela["endEntityID"]}\n'
                exe_temp = exe_temp + rela_str
            elif rela["direction"] == "two way":
                rela_str = f'{space}{rela["startEntityID"]} >> Edge() << {rela["endEntityID"]}\n'
                exe_temp = exe_temp + rela_str

    return exe_temp
