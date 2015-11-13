from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView

from group.models import Group
from group.group_service import group_exist
from group.group_service import create_group
from group.group_service import join_to_group
from group.group_service import get_member_joined_groups
# Create your views here.


class Join(APIView):
    '''
    Invite a person join a group
    '''
    def post(self, request):
        """
        Inviter invites Invitee join to group G,
        if G not exist, created a new group.

        post:

            {
                inviter: string,
                invitee: string,
                group: string // could be none, if no group id, create one
            }

        Returns:

            {
                status: HTTP status, // show if succeed update.
                group: string // group's unique name
            }

        ---
        parameters:
        - name: inviter
          descritpion: inviter account
          required: true
          type: string
          parameType: form

        - name: invitee
          descritpion: invitee account
          required: true
          type: string
          parameType: form

        - name: group
          descritpion: group unique name
          required: false
          type: string
          parameType: form

        """

        inviter = request.data.get('inviter', None)
        invitee = request.data.get('invitee', None)
        group_name = request.data.get('group', None)

        # category = 'H'
        if not group_name or not group_exist(group_name):
            group_name = create_group(creator=inviter)
            join_to_group(inviter, group_name)

        try:
            join_to_group(invitee, group_name)
            return Response({'status': status.HTTP_201_CREATED,
                             'group': group_name})
        except Exception as e:
            print e
            return Response({'status': status.HTTP_406_NOT_ACCEPTABLE})


class Member(APIView):
    '''
    1. Add a person to one group
    2. get one person's all incorported groups.
    '''
    def get(self, request, name):
        '''
        Gets one person's all incorporated groups.

        returns:

            {
            groups:{name:'group_name1'},
            }
        '''

        import pdb; pdb.set_trace();
        try:
            results = get_member_joined_groups(name)
            return Response({'status': status.HTTP_200_OK, 'data': results})
        except Exception as e:
            print e
            return Response({'status': status.HTTP_404_NOT_FOUND})


class GroupAPI(APIView):
    '''
    CRUD for a group
    '''

    def get_object(self, name):
        try:
            return Group.objects.get(name=name)
        except Exception as e:
            raise e

    def get(self, request, name, format=None):
        '''
        gets a group's information

        '''
        group = self.get_object(name)
        serializer = GroupSerializer(group)
        return Response({'status': status.HTTP_200_OK, 'data': serializer.data})

    def put(self, request, name, format=None):
        group = self.get_object(name)
        serializer = GroupSerializer(group, data=request.data)
        if serializer.is_valid():
            serializer.save()
            return Response({'status': status.HTTP_202_ACCEPTED,
                             'data': serializer.data})

        return Response({'status': status.HTTP_406_NOT_ACCEPTABLE})

    def delete(self, request, name, format=None):
        group = self.get_object(name)
        group.delete()
        return Response({'status': status.HTTP_204_NO_CONTENT})